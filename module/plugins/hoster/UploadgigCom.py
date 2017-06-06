# -*- coding: utf-8 -*-
import re

from module.network.HTTPRequest import BadHeader
from module.plugins.internal.SimpleHoster import SimpleHoster
from module.plugins.captcha.ReCaptcha import ReCaptcha
from module.plugins.internal.misc import json


class UploadgigCom(SimpleHoster):
    __name__ = "UploadgigCom"
    __type__ = "hoster"
    __pattern__ = r"https?://(?:www\.)?uploadgig\.com/file/download/(?P<ID>\w*)"
    __version__ = "0.01"
    __description__ = """Uploadgig.com hoster plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    INFO_PATTERN = r'<span class="filename">(?P<N>[^<]*)<span class="filesize">\[(?P<S>[\d.]*) (?P<U>KMGB]*)\]</span>'

    DIRECT_LINK_PATTERN = r'<a href="([^"]+)"><img src="[^"]*down.jpg"'

    def setup(self):
        self.resumeDownload = True
        self.multiDL = False

    def process(self, pyfile):
        self.log_debug('starting process...')
        self._prepare()
        try:
            self._preload()
        except BadHeader, e:
            # curiously, instead of wait messages, uploadgig gives us a 403 header reply saying "404 Page Not Found" based on our IP
            # so, if we get that, just wait 1h and retry
            # if the file really is offline, uploadgig gives us a 404 header reply saying "File not found", which is handled by check_errors()
            if e.code == 403 and re.search(r'404 Page Not Found', e.content) is not None:
                self.log_info(_("uploadgig refuses to give the file"))
                self.wait(3600, reconnect=True)
                self.restart("restarting upon encountering uploadgigs 403/404 error")

        self.grab_info()
        self.check_status()
        self.check_duplicates()

        if self.info.get('status', 7) != 2:
            self.check_errors()
            self.check_status()
        
        self.log_info(_("Processing as free download..."))
        self.handle_free(pyfile)

        if self.link:
            self.log_info(_("Downloading file from link " + str(self.link) + "..."))
            self.download(self.link, disposition=self.DISPOSITION)

    def handle_free(self, pyfile):
        # Captcha handling
        answer = dict()
        self.captcha = ReCaptcha(pyfile)
        for i in xrange(5):
            challenge, response = self.captcha.challenge()
            action, post_data = self.parse_html_form('dl_captcha_form')
            self.log_debug('parsed inputs: %s' % str(inputs))

            # Create post data
            post_data.update({'recaptcha_challenge_field': challenge,
                              'recaptcha_response_field': response})

            self.data = self.load(pyfile.url, post=post_data)

            self.log_debug('response was: %s' % self.data)

            answer = json.loads(self.data)

            if 'url' in self.data:
                self.captcha.correct()
                try:
                    self.wait(int(answer['cd']))
                except Exception:
                    self.wait(60)
                finally:
                    self.link = answer['url']
            else:
                self.log_info('Wrong captcha')
                self.invalidCaptcha()
        else:
            self.fail("All captcha attempts failed")


