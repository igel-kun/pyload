# -*- coding: utf-8 -*-

import operator
import random
import re

from module.plugins.captcha.ReCaptcha import ReCaptcha
from module.plugins.captcha.SolveMedia import SolveMedia
from module.plugins.internal.SimpleHoster import SimpleHoster
from module.plugins.internal.misc import html_unescape, parse_time, seconds_to_midnight, set_cookie


class XFSHoster(SimpleHoster):
    __name__    = "XFSHoster"
    __type__    = "hoster"
    __version__ = "0.76"
    __status__  = "stable"

    __pattern__ = r'^unmatchable$'
    __config__  = [("activated"   , "bool", "Activated"                                        , True),
                   ("use_premium" , "bool", "Use premium account if available"                 , True),
                   ("fallback"    , "bool", "Fallback to free download if premium fails"       , True),
                   ("chk_filesize", "bool", "Check file size"                                  , True),
                   ("max_wait"    , "int" , "Reconnect if waiting time is greater than minutes", 10  ),
                   ("min_size"    , "int" , "Minimum size of files to download"                , 0)]

    __description__ = """XFileSharing hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg"      , "zoidberg@mujmail.cz"),
                       ("stickell"      , "l.stickell@yahoo.it"),
                       ("Walter Purcaro", "vuolter@gmail.com"  )]


    PLUGIN_DOMAIN         = None

    DIRECT_LINK           = None
    LEECH_HOSTER          = True  #@NOTE: hould be set to `False` by default for safe, but I am lazy...

    NAME_PATTERN          = r'(Filename[ ]*:[ ]*</b>(</td><td nowrap>)?|name="fname"[ ]+value="|<[\w^_]+ class="(file)?name">)\s*(?P<N>.+?)(\s*<|")'
    SIZE_PATTERN          = r'(Size[ ]*:[ ]*</b>(</td><td>)?|File:.*>|</font>\s*\(|<[\w^_]+ class="size">)\s*(?P<S>[\d.,]+)\s*(?P<U>[\w^_]+)'

    OFFLINE_PATTERN       = r'(Not Found|file (?:was|has been)?\s*(?:removed|deleted)|no longer available|copyright (?:viola|infr|claim)|did\s*n.t comply(?:\s*\w+)* Terms of Use|File does not exist|file could not be found)'
    TEMP_OFFLINE_PATTERN  = r'server (?:is in )?maint[eai]*nance'

    WAIT_PATTERN          = r'<span id="countdown".*>(\d+)</span>|id="countdown" value=".*?(\d+).*?"'
    PREMIUM_ONLY_PATTERN  = r'available for Premium Users only'
    HAPPY_HOUR_PATTERN    = r'[Hh]appy hour'
    ERROR_PATTERN         = r'(?:class=["\']err["\'].*?>|<[Cc]enter><b>|>Error</td>|>\(ERROR:)(?:\s*<.+?>\s*)*(.+?)(?:["\']|<|\))'

    LINK_LEECH_PATTERN    = r'<h2>Download Link</h2>\s*<textarea.*?>(.+?)'

    CAPTCHA_PATTERN       = r'(https?://[^"\']+?/captchas?/[^"\']+)'
    CAPTCHA_BLOCK_PATTERN = r'>Enter code.*?<div.*?>(.+?)</div>'
    RECAPTCHA_PATTERN     = None
    SOLVEMEDIA_PATTERN    = None

    FORM_PATTERN          = None
    FORM_INPUTS_MAP       = None  #: Dict passed as `input_names` to `parse_html_form`


    def setup(self):
        self.chunk_limit     = -1 if self.premium else 1
        self.multiDL         = self.premium
        self.resume_download = self.premium


    def _set_xfs_cookie(self):
        cookie = (self.PLUGIN_DOMAIN, "lang", "english")
        if isinstance(self.COOKIES, list) and cookie not in self.COOKIES:
            self.COOKIES.insert(cookie)
        else:
            set_cookie(self.req.cj, *cookie)


    def _prepare(self):
        if not self.PLUGIN_DOMAIN:
            self.fail(_("Missing PLUGIN DOMAIN"))

        if self.COOKIES:
            self._set_xfs_cookie()

        if not self.LINK_PATTERN:
            pattern = r"(?:file: \"(.+?)\"|(https?://(?:www\.)?(?:[^/]*?%s|\d+\.\d+\.\d+\.\d+)(?:\:\d+)?(?:/d/|(?:/files)?/\d+/\w+/).+?)[\"'<])"
            self.LINK_PATTERN = pattern % self.PLUGIN_DOMAIN.replace('.', '\.')

        super(XFSHoster, self)._prepare()

        if self.DIRECT_LINK is None:
            self.direct_dl = self.premium


    def handle_free(self, pyfile):
        # don't download small files
        minSize = self.config.get('min_size')
        self.log_debug('filesize is %s, minimum is %s MB' % (str(pyfile.size), str(minSize)))
        if pyfile.size and minSize > 0:
            if pyfile.size < 1024*1024*minSize:
                self.fail('file is smaller than configured minimum')

        for i in xrange(1, 6):
            self.log_debug("Getting download link #%d..." % i)
            self.log_debug("using pattern %s" % str(self.LINK_PATTERN))

            self.check_errors()

            m = re.search(self.LINK_PATTERN, self.data, re.S)
            if m is not None:
                for link_match in m.groups():
                    if link_match:
                        self.link = link_match
                self.log_debug('found link: %s' % self.link)
                break

            m = re.search(self.LINK_PATTERN, self.data, re.MULTILINE | re.DOTALL)
            if m is not None:
                for link_match in m.groups():
                    if link_match:
                        self.link = link_match
                self.log_debug('found link with MULTILINE: %s' % self.link)
                break

            self.log_debug("Couldn't find the link, advancing to next layer...")
            self.data = self.load(pyfile.url,
                                  post=self._post_parameters(),
                                  redirect=False)

            if not "op=" in self.last_header.get('location', "op="):
                self.link = self.last_header.get('location')
                self.log_debug('found redirect to %s' % self.link)
                break

        else:
            if 'op' in data:
                self.error(_("Missing OP data after: ") + data['op'])

        self.log_debug('using link: %s' % self.link)


    def handle_premium(self, pyfile):
        return self.handle_free(pyfile)


    def handle_multi(self, pyfile):
        if not self.account:
            self.fail(_("Only registered or premium users can use url leech feature"))

        #: Only tested with easybytez.com
        self.data = self.load("http://www.%s/" % self.PLUGIN_DOMAIN)

        action, inputs = self.parse_html_form()

        upload_id = "%012d" % int(random.random() * 10 ** 12)
        action += upload_id + "&js_on=1&utype=prem&upload_type=url"

        inputs['tos'] = '1'
        inputs['url_mass'] = pyfile.url
        inputs['up1oad_type'] = 'url'

        self.log_debug(action, inputs)

        self.req.setOption("timeout", 600)  #: Wait for file to upload to easybytez.com

        self.data = self.load(action, post=inputs)

        self.check_errors()

        action, inputs = self.parse_html_form('F1')
        if not inputs:
            self.fail(msg=self.info.get('error') or _("TEXTAREA F1 not found"))

        self.log_debug(inputs)

        stmsg = inputs['st']

        if stmsg == 'OK':
            self.data = self.load(action, post=inputs)

        elif 'Can not leech file' in stmsg:
            self.retry(20, 3 * 60, _("Can not leech file"))

        elif 'today' in stmsg:
            self.retry(wait=seconds_to_midnight(), msg=_("You've used all Leech traffic today"))

        else:
            self.fail(stmsg)

        #: Get easybytez.com link for uploaded file
        m = re.search(self.LINK_LEECH_PATTERN, self.data)
        if m is None:
            self.error(_("LINK_LEECH_PATTERN not found"))

        self.link = self.load(m.group(1), just_header=True).get('location')


    def _post_parameters(self):
        if self.FORM_PATTERN or self.FORM_INPUTS_MAP:
            self.log_debug('using local FORM_PATTERN')
            action, inputs = self.parse_html_form(self.FORM_PATTERN or "", self.FORM_INPUTS_MAP or {})

            if inputs:
                self.log_debug('read: ')
                for key, val in inputs.iteritems():
                    self.log_debug('%s' % key)
                    self.log_debug('%s' % val)
        else:
            action, inputs = self.parse_html_form(input_names={'op': re.compile(r'^download')})

        if not inputs:
            action, inputs = self.parse_html_form('F1')
            if not inputs:
                self.fail(msg=self.info.get('error') or _("TEXTAREA F1 not found"))
        
        if hasattr(self, 'HIDDEN_POST_PARAMETERS'):
            self.log_debug('parsing additional parameters...')
            for inputtag in re.finditer(self.HIDDEN_POST_PARAMETERS, self.html):
                self.log_debug("adding hidden post parameter: %s = %s" % (inputtag.group('id'), inputtag.group('value')))
                inputs[inputtag.group('id')] = inputtag.group('value')
        else:
            self.log_debug('no additional parameters to parse...')

        self.log_debug(inputs)

        if 'op' in inputs:
            if "password" in inputs:
                password = self.get_password()
                if password:
                    inputs['password'] = password
                else:
                    self.fail(_("Missing password"))

            if not self.premium:
                m = re.search(self.WAIT_PATTERN, self.data)
                if m is not None:
                    try:
                        waitmsg = m.group(1).strip()

                    except (AttributeError, IndexError):
                        waitmsg = m.group(0).strip()

                    wait_time = parse_time(waitmsg)
                    self.set_wait(wait_time)
                    self.set_reconnect(False)
                    if wait_time < self.config.get('max_wait', 10) * 60:
                        self.handle_captcha(inputs)
                    self.wait()

                else:
                    self.handle_captcha(inputs)

                if 'referer' in inputs and len(inputs['referer']) == 0:
                    inputs['referer'] = self.pyfile.url

        else:
            inputs['referer'] = self.pyfile.url

        if self.premium:
            inputs['method_premium'] = "Premium Download"
            inputs.pop('method_free', None)
        else:
            inputs['method_free'] = "Free Download"
            inputs.pop('method_premium', None)

        return inputs


    def handle_captcha(self, inputs):
        m = re.search(self.CAPTCHA_PATTERN, self.data)
        if m is not None:
            captcha_url = m.group(1)
            inputs['code'] = self.captcha.decrypt(captcha_url)
            return

        m = re.search(self.CAPTCHA_BLOCK_PATTERN, self.data, re.S)
        if m is not None:
            captcha_div = m.group(1)
            numerals    = re.findall(r'<span.*?padding-left\s*:\s*(\d+).*?>(\d)</span>', html_unescape(captcha_div))

            self.log_debug(captcha_div)

            inputs['code'] = "".join(a[1] for a in sorted(numerals, key=operator.itemgetter(0)))

            self.log_debug("Captcha code: %s" % inputs['code'], numerals)
            return

        recaptcha = ReCaptcha(self.pyfile)
        try:
            captcha_key = re.search(self.RECAPTCHA_PATTERN, self.data).group(1)

        except Exception:
            captcha_key = recaptcha.detect_key()

        else:
            self.log_debug("ReCaptcha key: %s" % captcha_key)

        if captcha_key:
            self.captcha = recaptcha
            inputs['recaptcha_response_field'], inputs['recaptcha_challenge_field'] = recaptcha.challenge(captcha_key)
            return

        solvemedia = SolveMedia(self.pyfile)
        try:
            captcha_key = re.search(self.SOLVEMEDIA_PATTERN, self.data).group(1)

        except Exception:
            captcha_key = solvemedia.detect_key()

        else:
            self.log_debug("SolveMedia key: %s" % captcha_key)

        if captcha_key:
            self.captcha = solvemedia
            inputs['adcopy_response'], inputs['adcopy_challenge'] = solvemedia.challenge(captcha_key)
