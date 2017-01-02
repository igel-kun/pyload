# -*- coding: utf-8 -*-


import re
from module.plugins.internal.SimpleHoster import SimpleHoster
from module.plugins.captcha.ReCaptcha import ReCaptcha


class BitshareCom(DeadHoster):
    __name__    = "BitshareCom"
    __type__    = "hoster"
    __version__ = "0.62"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?bitshare\.com/(files/)?(?(1)|\?f=)(?P<ID>\w+)(?(1)/(?P<NAME>.+?)\.html)'
    __config__  = [("activated"   , "bool", "Activated", True)]

    __description__ = """Bitshare.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", None)]

    INFO_PATTERN = r'<h1>Downloading (?P<N>.*?) - (?P<S>[\d.]*) (?P<U>.*?)</h1>'
    OFFLINE_PATTERN = r'not found'
    AJAX_DL_PATTERN = r'var ajaxdl = "([^"]*)"'

    def ajax_request(self, request, additional_post = {}):
        post_data = additional_post
        post_data.update({"request": request, "ajaxid": self.ajax_id})
        response = self.load("http://bitshare.com/files-ajax/" + self.file_id + "/request.html", post=post_data)
        
        self.log_debug("ajax response: " + response)
        return response

    def handle_captcha(self):
        self.captcha = ReCaptcha(self.pyfile)
        response, challenge = self.captcha.challenge()
        post_data = {'recaptcha_challenge_field': challenge,
                     'recaptcha_response_field' : response}
        return self.ajax_request("validateCaptcha", post_data)


    def handle_free(self, pyfile):
        self.file_id = re.search(self.__pattern__, pyfile.url).group("ID")
        self.ajax_id = re.search(self.AJAX_DL_PATTERN, self.data).group(1)

        file_type, wait_time, captcha = self.ajax_request("generateID").split(":")

        if "1" in captcha:
            for i in xrange(5):
                response = self.handle_captcha()
                if 'SUCCESS' in response:
                    self.captcha.correct()
                    break
                else:
                    self.info(_("Wrong captcha"))
                    self.captcha.invalid()
            else:
                self.retry_captcha()

        #TODO: parallelize wait
        self.wait(int(wait_time))

        self.link = self.ajax_request("getDownloadURL").split(":")[1]



