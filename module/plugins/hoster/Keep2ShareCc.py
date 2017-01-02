# -*- coding: utf-8 -*-

import re
import urlparse

from module.plugins.captcha.ReCaptcha import ReCaptcha
from module.plugins.internal.SimpleHoster import SimpleHoster


class Keep2ShareCc(SimpleHoster):
    __name__    = "Keep2ShareCc"
    __type__    = "hoster"
    __version__ = "0.32"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?(keep2share|k2s|keep2s)\.cc/file/(?P<ID>\w+)'
    __config__  = [("activated"   , "bool", "Activated"                                        , True),
                   ("use_premium" , "bool", "Use premium account if available"                 , True),
                   ("fallback"    , "bool", "Fallback to free download if premium fails"       , True),
                   ("chk_filesize", "bool", "Check file size"                                  , True),
                   ("max_wait"    , "int" , "Reconnect if waiting time is greater than minutes", 10  )]

    __description__ = """Keep2Share.cc hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell"      , "l.stickell@yahoo.it"       ),
                       ("Walter Purcaro", "vuolter@gmail.com"         ),
                       ("GammaC0de"     , "nitzo2001[AT]yahoo[DOT]com")]

    DIRECT_LINK = False  #@TODO: Recheck in v0.4.10
    DISPOSITION = False  #@TODO: Recheck in v0.4.10

    NAME_PATTERN = r'File: <span>(?P<N>.+?)</span>'
    SIZE_PATTERN = r'Size: (?P<S>.+?)</div>'

    OFFLINE_PATTERN      = r'File not found or deleted|Sorry, this file is blocked or deleted|Error 404'
    TEMP_OFFLINE_PATTERN = r'Downloading blocked due to'

    LINK_FREE_PATTERN    = r'"([^"]+?url.html\?file=.+?)"|window\.location\.href = \'(.+?)\';'
    LINK_PREMIUM_PATTERN = r'window\.location\.href = \'(.+?)\';'
    UNIQUE_ID_PATTERN    = r"data: {uniqueId: '(?P<uID>\w+)', free: 1}"

    PREMIUM_ONLY_PATTERN = r'only for premium (?:members|users)'

    CAPTCHA_PATTERN = r'src="(/file/captcha\.html.+?)"'

    WAIT_PATTERN         = r'Please wait ([\d:]+) to download this file'
    TEMP_ERROR_PATTERN   = r'>\s*(Download count files exceed|Traffic limit exceed|Free account does not allow to download more than one file at the same time)'
    ERROR_PATTERN        = r'>\s*(Free user can\'t download large files|You no can access to this file|file is no longer available|This is private file)'


    # a problem with keep2share is that it sometimes forwards requests to other URLs (like k2s)
    # for example:
    # if we try to download a file from keep2s.cc but get forwarded to k2s.cc,
    # then, the download request goes to k2s.cc but the captcha request goes to keep2s.cc
    # this causes correctly solved captchas to be considered wrong :(
    # to combat this, the following function follows all redirects and updates self.pyfile.url
    def setup(self):
        header = self.load(self.pyfile.url, just_header = True)
        while 'location' in header:
            self.log_debug('got redirected to %s' % str(header['location']))
            self.pyfile.url = header['location']
            header = self.load(self.pyfile.url, just_header = True)
        super(Keep2ShareCc, self).setup()


    def handle_free(self, pyfile):
        self.check_errors()

        m = re.search(r'<input type="hidden" name="slow_id" value="(.+?)">', self.data)
        if m is None:
            self.error(_("Slow-ID pattern not found"))

        self.fid  = m.group(1)

        self.data = self.load(pyfile.url, post={'yt0': '',
                                                'slow_id': self.fid})

        # self.log_debug(self.fid)
        self.log_debug('URL: %s' % pyfile.url)

        self.check_errors()

        m = re.search(self.LINK_FREE_PATTERN, self.data)
        if m is None:
            self.handle_captcha()

            m = re.search(r'<div id="download-wait-timer".*>\s*(\d+).+?</div>', self.data)
            if m:
                self.wait(m.group(1), reconnect=False)

            # get the uniqueId from the html code
            m = re.search(self.UNIQUE_ID_PATTERN, self.data)
            if m is None:
                self.error(_("Unique-ID pattern not found"))

            self.data = self.load(pyfile.url, post={'uniqueId': m.group('uID'),
                                                    'free': '1'})

            m = re.search(self.LINK_FREE_PATTERN, self.data)
            if m is None:
                self.error(_("Free download link not found"))

        # if group 1 did not match, check group 2
        self.link = m.group(1) if m.group(1) else m.group(2)


    def handle_captcha(self, url):
        post_data = {'free'               : 1,
                     'freeDownloadRequest': 1,
                     'uniqueId'           : self.fid,
                     'yt0'                : ''}

        m = re.search(r'id="(captcha-form)"', self.data)
        if m is not None:
            self.log_debug("Captcha form found", m.group(0))
            m = re.search(self.CAPTCHA_PATTERN, self.data)

            if m is not None:
                captcha_url = urlparse.urljoin(self.pyfile.url, m.group(1))
                post_data['CaptchaForm[code]'] = self.captcha.decrypt(captcha_url)

            else:
                self.captcha = ReCaptcha(self.pyfile)
                response, challenge = self.captcha.challenge()
                post_data.update({'recaptcha_challenge_field': challenge,
                                  'recaptcha_response_field' : response})

            self.data = self.load(self.pyfile.url, post=post_data)

            if 'verification code is incorrect' in self.data:
                self.retry_captcha()

            else:
                self.captcha.correct()

