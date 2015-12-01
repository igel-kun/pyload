# -*- coding: utf-8 -*-

import pycurl
import re
import time

from module.common.json_layer import json_loads
from module.plugins.captcha.ReCaptcha import ReCaptcha
from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class DatafileCom(SimpleHoster):
    __name__    = "DatafileCom"
    __type__    = "hoster"
    __version__ = "0.01"

    __pattern__ = r'https?://(?:www\.)?(?:datafile|wcrypt)\.com/.*'
    __description__ = """Rapidu.net hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("prOq", "")]


    INFO_PATTERN    = r'<div class="file-name">(?P<N>.*?)</div>.*<div class="file-size">Filesize: .*?(?P<S>[\d.]+)\s(?P<U>\w+)</'
    OFFLINE_PATTERN = r'<h1>404'
    ERROR_PATTERN = r'<div class="error">'
    RECAPTCHA_KEY_PATTERN = r'"https?://www.google.com/recaptcha/api/challenge?k=(.*?)">'
    PREMIUM_ONLY_PATTERN  = r'downloaded only by users with Premium'

    def setup(self):
        self.resumeDownload = True
        self.multiDL        = self.premium


    def handle_free(self, pyfile):
        self.req.http.lastURL = pyfile.url
        self.req.http.c.setopt(pycurl.HTTPHEADER, ["X-Requested-With: XMLHttpRequest"])

        jsvars = self.getJsonResponse("https://rapidu.net/ajax.php",
                                      get={'a': "getLoadTimeToDownload"},
                                      post={'_go': ""},
                                      decode=True)

        if str(jsvars['timeToDownload']) is "stop":
            t = (24 * 60 * 60) - (int(time.time()) % (24 * 60 * 60)) + time.altzone

            self.log_info("You've reach your daily download transfer")

            self.retry(10, 10 if t < 1 else None, _("Try tomorrow again"))  #@NOTE: check t in case of not synchronised clock

        else:
            self.wait(int(jsvars['timeToDownload']) - int(time.time()))

        recaptcha = ReCaptcha(self)
        response, challenge = recaptcha.challenge(self.RECAPTCHA_KEY)

        jsvars = self.getJsonResponse("https://rapidu.net/ajax.php",
                                      get={'a': "getCheckCaptcha"},
                                      post={'_go'     : "",
                                            'captcha1': challenge,
                                            'captcha2': response,
                                            'fileId'  : self.info['pattern']['ID']},
                                      decode=True)

        if jsvars['message'] == 'success':
            self.link = jsvars['url']


    def getJsonResponse(self, *args, **kwargs):
        res = self.load(*args, **kwargs)
        if not res.startswith('{'):
            self.retry()

        self.log_debug(res)

        return json_loads(res)


getInfo = create_getInfo(DatafileCom)
