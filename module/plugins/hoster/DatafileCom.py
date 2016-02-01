# -*- coding: utf-8 -*-

import pycurl
import re
import time
from urlparse import urlparse

from module.common.json_layer import json_loads
from module.plugins.captcha.ReCaptcha import ReCaptcha
from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class DatafileCom(SimpleHoster):
    __name__    = "DatafileCom"
    __type__    = "hoster"
    __version__ = "0.01"

    __pattern__ = r'https?://(?:www\.)?(?:datafile|wcrypt)\.com/\w*/(?P<ID>\w+)'
    __description__ = """Datafile & Wcrypt hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("prOq", ""),
                       ("igel", "")]


    INFO_PATTERN    = r'<div class="file-name">(?P<N>.*?)</div>.*<div class="file-size">Filesize: .*?(?P<S>[\d.]+)\s(?P<U>\w+)</'
    OFFLINE_PATTERN = r'<h1>404'
    ERROR_PATTERN = r'<div class="error">'
    PREMIUM_ONLY_PATTERN  = r'can be downloaded only by users.*Premium account'
    WAIT_TIME = r'exceeded your free.*download limit'
    DELAY_PATTERN = r"counter.contdownTimer\('(?P<time>\d+)'"
    DL_LIMIT_PATTERN = r'You are downloading another file at this moment.'

    def setup(self):
        self.resumeDownload = True
        self.multiDL        = self.premium

    def handle_free(self, pyfile):
        self.check_errors()
        self.req.http.lastURL = pyfile.url
        self.req.http.c.setopt(pycurl.HTTPHEADER, ["X-Requested-With: XMLHttpRequest"])

        parse = urlparse(pyfile.url)
        base = parse.scheme + '://' + parse.netloc
        ajax_target = base + '/files/ajax.html'
        
        m = re.search(self.DELAY_PATTERN, self.data)
        if m is not None:
            delay = m.group('time')
        else:
            # default delay to 2min
            delay = 120
        
        m = re.search(r'google.com/recaptcha/api/challenge.*"', self.data)
        self.log_debug('found captcha: %s' % m.group(0))
        
        recaptcha = ReCaptcha(self)
        response, challenge = recaptcha.challenge()

        jsvars = self.getJsonResponse(ajax_target,
                                      post={'doaction' : "validateCaptcha",
                                            'recaptcha_challenge_field': challenge,
                                            'recaptcha_response_field': response,
                                            'fileid'  : self.info['pattern']['ID']},
                                      decode=True) 

        
        if jsvars['success'] == 1:
            token = jsvars['token']
            self.captcha.correct()
        else:
            self.retry_captcha()
        
        self.log_debug('captcha was good, got token %s, now waiting %s seconds' % (str(token), str(delay)) )
        self.wait(delay)
 
        jsvars = self.getJsonResponse(ajax_target,
                                      post={'doaction' : "getFileDownloadLink",
                                            'recaptcha_challenge_field': challenge,
                                            'recaptcha_response_field': response,
                                            'token' : token,
                                            'fileid' : self.info['pattern']['ID']},
                                      decode=True)
        
        if 'success' in jsvars and jsvars['success'] == 1:
            self.link = jsvars['link']
        else:
            self.error(_("Free download link not found"))


    def getJsonResponse(self, *args, **kwargs):
        res = self.load(*args, **kwargs)
        if not res.startswith('{'):
            self.retry()

        self.log_debug(res)

        return json_loads(res)


getInfo = create_getInfo(DatafileCom)
