# -*- coding: utf-8 -*-

import re

from ..captcha.ReCaptcha import ReCaptcha
from ..internal.SimpleHoster import SimpleHoster


class UpstoreNet(SimpleHoster):
    __name__ = "UpstoreNet"
    __type__ = "hoster"
    __version__ = "0.17"
    __status__ = "testing"

    __pattern__ = r'https?://(?:www\.)?(?:upstore\.net|upsto\.re)/(?P<ID>\w+)'
    __config__ = [("activated", "bool", "Activated", True),
                  ("use_premium", "bool", "Use premium account if available", True),
                  ("fallback", "bool", "Fallback to free download if premium fails", True),
                  ("chk_filesize", "bool", "Check file size", True),
                  ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10)]

    __description__ = """Upstore.Net File Download Hoster"""
    __license__ = "GPLv3"
    __authors__ = [("igel", "igelkun@myopera.com"),
                   ("GammaC0de", "nitzo2001[AT]yahoo[DOT]com")]

    INFO_PATTERN = r'<div class="comment">.*?</div>\s*\n<h2 style="margin:0">(?P<N>.*?)</h2>\s*\n<div class="comment">\s*\n\s*(?P<S>[\d.,]+) (?P<U>[\w^_]+)'
    OFFLINE_PATTERN = r'<span class="error">File (?:not found|was deleted).*</span>'

    PREMIUM_ONLY_PATTERN = r'available only for Premium'
    LINK_FREE_PATTERN = r'<a href="(https?://.*?)" target="_blank"><b>'

    URL_REPLACEMENTS = [(__pattern__ + ".*", r'https://upstore.net/\g<ID>')]

    ERROR_PATTERN = r'(?:Please|You should) wait .*? ?before downloading next'
    WAIT_PATTERN = r'var sec = (\d+)'
    RECAPTCHA_KEY = "6LemftkSAAAAAJy5WVFbD9OrS7KHfLg5nUsDpTyj"

    COOKIES = [("upstore.net", "lang", "en")]

    def handle_free(self, pyfile):
        #: STAGE 1: get link to continue
        post_data = {'hash': self.info['pattern']['ID'],
                     'free': 'Slow download'}
        self.data = self.load(pyfile.url, post=post_data)
        self.check_errors()

        #: STAGE 2: solve captcha and wait
        #: First get the infos we need: self.captcha key and wait time
        m = re.search(self.WAIT_PATTERN, self.data)
        if m is None:
            self.error("Wait pattern not found")

        #: gotta wait before solving the captcha
        self.wait(int(m.group(1)))

        #: then, handle the captcha
        self.captcha = ReCaptcha(self.pyfile)

        captcha_key = self.captcha.detect_key()
        if captcha_key is None:
            self.log_warning(_("captcha key not found, using hardcoded key %s") % self.RECAPTCHA_KEY)
            captcha_key = self.RECAPTCHA_KEY
        elif captcha_key != self.RECAPTCHA_KEY:
            self.log_warning(_("detected key differs from hardcoded one, please report this as a plugin bug"))

        post_data = {'hash': self.info['pattern']['ID'],
                     'free': 'Get download link'}
        post_data['g-recaptcha-response'], _ = self.captcha.challenge(captcha_key)

        self.data = self.load(pyfile.url, post=post_data)

        # check whether the captcha was wrong
        if "check failed" in self.data:
            self.captcha.invalid()
        else:
            self.captcha.correct()

        # STAGE 3: get direct link or wait time
        self.check_errors()
        m = re.search(self.LINK_FREE_PATTERN, self.data)
        if m is not None:
            self.link = m.group(1)
