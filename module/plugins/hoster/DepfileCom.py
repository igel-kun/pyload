# -*- coding: utf-8 -*-


import re
import urlparse
from module.common.JsEngine import JsEngine
from module.plugins.internal.SimpleHoster import SimpleHoster


class DepfileCom(SimpleHoster):
    __name__ = "DepfileCom"
    __type__ = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'(?:https?://)?(?:www\.)*depfile\.com/'
    __description__ = """depfile.com plugin"""
    __license__     = "GPLv3"
    __authors__ = [("igel", "")]

    LINK_FREE_PATTERN = r''
    NAME_PATTERN = r'<th>File name:</th>\n\s*<td>(?P<N>[^<]*)</td>'
    ERROR_PATTERN = r"<p class=['\"](?:notice|error).*</p>"
    SIZE_PATTERN = r'<th>Size:</th>\n\s*<td>(?P<S>[^<]*)</td>'
    WAIT_PATTERN = 'no less than (.*?) should pass'
    SEARCH_TYPE = {'NAME_PATTERN': re.MULTILINE, 'SIZE_PATTERN': re.MULTILINE}


    def handle_free(self, pyfile):
        for i in xrange(1,5):
            vvcid = re.search(r"name='vvcid' value='([^']*)'", self.data).group(1)
            # they have a spelling error in their html...
            captcha_img = re.search(r"class='vvc_i[ma]*ge'.*?src='([^']*)'", self.data).group(1)
            # fix relative URL
            captcha_response = self.captcha.decrypt(urlparse.urljoin(pyfile.url, captcha_img), ocr="VerticalShift")

            self.data = self.load(pyfile.url, post={'vvcid': vvcid, 'verifycode': captcha_response, 'FREE':'Low Speed Download'})

            #self.log_debug(self.data)
            if re.search('Wrong CAPTCHA', self.data):
                self.captcha.invalid()
                continue
            elif re.search('Download limit for free user', self.data):
                self.retry(wait = 2*60*60)
            else:
                self.captcha.correct()
                self.set_wait(60)
                
                js = JsEngine()
                varname = re.search(r'getElementById\("wait_url"\).innerHTML=.*?\+(\w*)\+', self.data).group(1)
                js_code = (re.search(r'var .*_keyStr.*', self.data).group(0) + ';' +
                        re.search(r'var '+str(varname)+'=.*', self.data).group(0) +
                        js.print_command() + '('+str(varname)+');')
                self.link = js.eval_raw(js_code)
                self.log_debug('using link ' + str(self.link))
                if self.link == '':
                    raise ValueError(js_code)
                self.wait()
                break

