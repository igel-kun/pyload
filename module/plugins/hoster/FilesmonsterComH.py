# -*- coding: utf-8 -*-

import re

from ..internal.misc import json, search_pattern, parse_time
from ..internal.SimpleHoster import SimpleHoster
from ..captcha.ReCaptcha import ReCaptcha

class FilesmonsterComH(SimpleHoster):
    __name__ = "FilesmonsterComH"
    __type__ = "hoster"
    __pattern__ = r"https?://(?:w{3}\.)?filesmonster\.com/download"
    __version__ = "0.02"
    __description__ = """Filesmonster.com Hoster Plugin"""
    __author_name__ = [("igel", None)]
    # filesmonster allows downloads in fairly rapid succession, so we'll set the default max_wait to 1 Minute instead of 10
    __config__ = [("activated", "bool", "Activated", True),
                  ("use_premium", "bool", "Use premium account if available", True),
                  ("fallback", "bool", "Fallback to free download if premium fails", True),
                  ("chk_filesize", "bool", "Check file size", True),
                  ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 1)]

    DL_LIMIT_PATTERN = r"Next download will be available in ([0-9 a-z]+)"
    PREMIUM_ONLY_PATTERN = r'need Premium membership to download'
    INFO_PATTERN =  'File name:.*?<td.*?>(?P<N>.*?)</td>.*?File size:.*?<td.*?>(?P<S>.*?)</td>', re.MULTILINE | re.DOTALL
    
    LINK_PATTERN =    r"onclick=\"get_link\('([^']*)'\)"
    WRONG_CAPTCHA_PATTERN = r"<p class=\"error\">Wrong captcha"

    RFT_PATTERN = r"rftUrl = '([^']*)';.*step2UrlTemplate = '([^']*)';", re.MULTILINE | re.DOTALL
    WAIT_TIME_PATTERN = r"var timeout='([0-9]*)'"
    RFT_MAGIC = '!!!'
    #TODO: parse RFT_MAGIC in step2 from:
    #       action: step2UrlTemplate.replace('!!!', link.dlcode),

    def handle_free(self, pyfile):
        # step 1: parse free download URL and click on it
        action, inputs = self.parse_html_form('id="slowdownload')
        if not action:
            self.log_debug('could not parse form with id starting with "slowdownload":\n%s' % self.data)
            self.fail()

        self.log_debug('parsed form: %s with inuts %s' % (str(action), str(inputs)))
        self.data = self.load(action)

        # step 2: parse rtfUrl and step2url template
        m = search_pattern(self.RFT_PATTERN, self.data)
        if not m:
            self.log_debug('could not parse rftUrl from:\n%s' % self.data)
            self.fail()

        rftUrl = m.group(1)
        step2url = m.group(2)
        self.log_debug('parsed rftUrl: %s and step2template: %s' % (rftUrl, step2url))

        if not self.RFT_MAGIC in step2url:
            self.log_debug('')

        self.data = self.load(self.fixurl(rftUrl))
        self.log_debug('parsing JSON response: %s' % self.data)
        res = json.loads(self.data)

        #step 3: check response status
        if (res['status'] != 'success') or not ('volumes' in res) or not ('dlcode' in res['volumes'][0]):
            self.log_debug('cannot parse dlcode from response: %s' % str(res))
            self.fail()
        
        #step 4: get next URL by replacing RFT_MAGIC (hardcoded to "!!!" for now) in the step2url template
        link = res['volumes'][0]
        self.log_debug('replacing %s --> %s in %s' % (self.RFT_MAGIC, link['dlcode'], step2url))
        step2url = self.fixurl(step2url.replace(self.RFT_MAGIC, link['dlcode']))
        self.data = self.load(step2url)

        self.captcha = ReCaptcha(self.pyfile)
        for i in range(5):
            #step 5: handle captcha
            challenge, response = self.captcha.challenge()
            self.data = self.load(step2url, post={'g-recaptcha-response': response})

            #step 6: wait and download
            m = search_pattern(self.WAIT_TIME_PATTERN, self.data)
            if not m:
                self.set_wait(30)
            else:
                self.set_wait(parse_time(m.group(1)))
                    
            m = search_pattern(self.LINK_PATTERN, self.data)
            if m is not None:
                self.captcha.correct()
                self.wait()
                url = self.fixurl(m.group(1))
                self.data = self.load(url)
                res = json.loads(self.data)
                if not 'url' in res:
                    self.log_debug('cannot parse json response: %s' % str(res))
                    self.fail()
                else:
                    self.link = res['url']
                    break
        else:
            self.log_debug('could not parse link pattern from response: %s' % self.data)
            self.error(_("could not parse link pattern"))


