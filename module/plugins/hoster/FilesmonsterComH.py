# -*- coding: utf-8 -*-

############################################################################
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Affero General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Affero General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
############################################################################

import re

from module.lib.bottle import json_loads
from module.plugins.internal.SimpleHoster import SimpleHoster
from module.plugins.captcha.ReCaptcha import ReCaptcha


class FilesmonsterComH(SimpleHoster):
    __name__ = "FilesmonsterComH"
    __type__ = "hoster"
    __pattern__ = r"http://(?:w{3}\.)?filesmonster\.com/+dl/.*"
    __version__ = "0.01"
    __description__ = """Filesmonster.com Hoster Plugin"""
    __author_name__ = ("igel")

    BASE_URL = "http://www.filesmonster.com/"
    WAIT_TIME_PATTERN = r"Please wait\s*<span id='sec'>(\d+)</span>"
    LINK_PATTERN = r"onclick=\"get_link\('(.*?)'\)"
    TEMPORARY_OFFLINE_PATTERN = r"You have started to download"
    NEXT_FILE_WAIT_PATTERN = r"will be available for download in (\d+)"
    WRONG_CAPTCHA_PATTERN = r"<p class=\"error\">Wrong captcha"

    def handle_captcha(self, pyfile):
        self.captcha = ReCaptcha(pyfile)
        for i in range(5):
          challenge, response = self.captcha.challenge()

          self.data = self.load(self.pyfile.url, cookies=True, post={
            "recaptcha_challenge_field": challenge,
            "recaptcha_response_field": response,
          })

          if self.WRONG_CAPTCHA_PATTERN in self.data:
            self.captcha.invalid()
          else:
            self.captcha.correct()
            break
        else:
          self.fail("No valid captcha solution received")
      else:
        self.parseError('could not find the captcha key')


    def handle_wait(self):
      m = re.search(self.WAIT_TIME_PATTERN, self.data)
      if m:
        self.log_debug('waiting %s seconds' % m.group(1))
        self.setWait(m.group(1))
        self.wait()
      else:
        self.parseError('could not parse the wait time')

    def get_link(self):
      m = re.search(self.LINK_PATTERN, self.data)
      if m:
        self.log_debug('reading JSON data from ' + m.group(1))
        json = json_loads(self.load(self.BASE_URL + m.group(1), decode=True, cookies=True))
        if not json['error']:
          return json['url']
        else:
          self.parseError('unhandled json error: ' + json['error'])
      else:
        self.parseError('could not parse the JSON link')


    def getFileInfo(self):
      m = re.search(self.TEMPORARY_OFFLINE_PATTERN, self.data)
      if m:
        m = re.search(self.NEXT_FILE_WAIT_PATTERN, self.data)
        if m:
          wait_time = 60 * int(m.group(1))
          self.log_debug('need to wait %d sec to download the file' % wait_time)
          # wait time for next file is usually in minutes
          self.setWait(wait_time, reconnect = True)
          self.wait()
          self.retry()
        else:
          self.parseError('error parsing time to wait for the next file')
      else:
        self.log_debug('file can be downloaded')



    def handle_free(self):
      self.data = self.load(self.pyfile.url, decode=True, cookies=True)
      # filesmonster starts off with a captcha, so polite...
      self.handle_captcha(self.pyfile)
      # next, we get to wait
      self.handle_wait()
      # and finally, we can get the link
      self.link = self.get_link()


