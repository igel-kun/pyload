# -*- coding: utf-8 -*-
# @author: RaNaN

from __future__ import with_statement

import cStringIO
import codecs
import httplib
import logging
import urllib

import pycurl

from module.plugins.Plugin import Abort, Fail

from module.plugins.internal.misc import encode


bad_headers = range(400, 404) + range(405, 600)

unofficial_errors = {440: "Login Timeout - The client's session has expired and must log in again.",
                     449: "Retry With - The server cannot honour the request because the user has not provided the required information",
                     451: "Redirect - Unsupported Redirect Header",
                     520: "Unknown Error",
                     521: "Web Server Is Down - The origin server has refused the connection from CloudFlare",
                     522: "Connection Timed Out - CloudFlare could not negotiate a TCP handshake with the origin server",
                     523: "Origin Is Unreachable - CloudFlare could not reach the origin server",
                     524: "A Timeout Occurred - CloudFlare did not receive a timely HTTP response",
                     525: "SSL Handshake Failed - CloudFlare could not negotiate a SSL/TLS handshake with the origin server",
                     526: "Invalid SSL Certificate - CloudFlare could not validate the SSL/TLS certificate that the origin server presented"}

class BadHeader(Exception):

    def __init__(self, code, content=""):
        int_code = int(code)
        Exception.__init__(self, "Bad server response: %s %s" % (code, httplib.responses[int_code] if int_code in httplib.responses else unofficial_errors.get(int_code, "unknown error")))
        self.code = code
        self.content = content


class HTTPRequest(object):

    def __init__(self, cookies=None, options=None):
        self.c = pycurl.Curl()
        self.rep = None

        self.cj = cookies  #: cookiejar

        self.lastURL = None
        self.lastEffectiveURL = None
        self.abort = False
        self.code = 0  #: last http code

        self.header = ""

        self.headers = []  #: temporary request header

        self.initHandle()
        self.setInterface(options)

        self.c.setopt(pycurl.WRITEFUNCTION, self.write)
        self.c.setopt(pycurl.HEADERFUNCTION, self.writeHeader)

        self.log = logging.getLogger("log")


    def initHandle(self):
        """Sets common options to curl handle"""
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 10)
        self.c.setopt(pycurl.CONNECTTIMEOUT, 45)
        self.c.setopt(pycurl.NOSIGNAL, 1)
        self.c.setopt(pycurl.NOPROGRESS, 1)
        if hasattr(pycurl, "AUTOREFERER"):
            self.c.setopt(pycurl.AUTOREFERER, 1)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.c.setopt(pycurl.LOW_SPEED_TIME, 60)
        self.c.setopt(pycurl.LOW_SPEED_LIMIT, 5)
        if hasattr(pycurl, "USE_SSL"):
            self.c.setopt(pycurl.USE_SSL, pycurl.CURLUSESSL_TRY)

        #self.c.setopt(pycurl.VERBOSE, 1)

        self.c.setopt(pycurl.USERAGENT,
                      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0")

        if pycurl.version_info()[7]:
            self.c.setopt(pycurl.ENCODING, "gzip, deflate")
        self.c.setopt(pycurl.HTTPHEADER, ["Accept: */*",
                                          "Accept-Language: en-US, en",
                                          "Accept-Charset: ISO-8859-1, utf-8;q=0.7,*;q=0.7",
                                          "Connection: keep-alive",
                                          "Keep-Alive: 300",
                                          "Expect:"])


    def setInterface(self, options):

        interface, proxy, ipv6 = options['interface'], options['proxies'], options['ipv6']

        if interface and interface.lower() != "none":
            self.c.setopt(pycurl.INTERFACE, str(interface))

        if proxy:
            if proxy['type'] == "socks4":
                self.c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS4)
            elif proxy['type'] == "socks5":
                self.c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
            else:
                self.c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)

            self.c.setopt(pycurl.PROXY, str(proxy['ip']))
            self.c.setopt(pycurl.PROXYPORT, proxy['port'])

            if proxy['username']:
                self.c.setopt(pycurl.PROXYUSERPWD, str("%s:%s" % (proxy['username'], proxy['password'])))

        if ipv6:
            self.c.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_WHATEVER)
        else:
            self.c.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)

        if options and "auth" in options:
            self.c.setopt(pycurl.USERPWD, str(options['auth']))

        if options and "timeout" in options:
            self.c.setopt(pycurl.LOW_SPEED_TIME, options['timeout'])


    def addCookies(self):
        """Put cookies from curl handle to cj"""
        if self.cj:
            self.cj.addCookies(self.c.getinfo(pycurl.INFO_COOKIELIST))


    def getCookies(self):
        """Add cookies from cj to curl handle"""
        if self.cj:
            for c in self.cj.getCookies():
                self.c.setopt(pycurl.COOKIELIST, c)
        return


    def clearCookies(self):
        self.c.setopt(pycurl.COOKIELIST, "")


    def setRequestContext(self, url, get, post, referer, cookies, multipart=False):
        """Sets everything needed for the request"""

        url = urllib.quote(encode(url).strip(), safe="%/:=&?~#+!$,;'@()*[]")  #@TODO: recheck

        if get:
            get = urllib.urlencode(get)
            url = "%s?%s" % (url, get)

        self.c.setopt(pycurl.URL, url)
        self.c.lastUrl = url

        if post:
            self.c.setopt(pycurl.POST, 1)
            if not multipart:
                if type(post) == unicode:
                    post = str(post)  #: unicode not allowed
                elif type(post) == str:
                    pass
                else:
                    post = urllib.urlencode(dict((encode(x), encode(y)) for x, y in dict(post).iteritems()))

                self.c.setopt(pycurl.POSTFIELDS, post)
            else:
                post = [(x, encode(y)) for x, y in post.iteritems()]
                self.c.setopt(pycurl.HTTPPOST, post)
        else:
            self.c.setopt(pycurl.POST, 0)

        if referer and self.lastURL:
            self.c.setopt(pycurl.REFERER, str(self.lastURL))

        if cookies:
            self.c.setopt(pycurl.COOKIEFILE, "")
            self.c.setopt(pycurl.COOKIEJAR, "")
            self.getCookies()


    def load(self, url, get={}, post={}, referer=True, cookies=True, just_header=False, multipart=False, decode=False, follow_location=True, save_cookies=True):
        """Load and returns a given page"""

        self.setRequestContext(url, get, post, referer, cookies, multipart)

        self.rep = cStringIO.StringIO()

        self.header = ""

        self.c.setopt(pycurl.HTTPHEADER, self.headers)

        if post:
            self.c.setopt(pycurl.POST, 1)
        else:
            self.c.setopt(pycurl.HTTPGET, 1)

        if not follow_location:
            self.c.setopt(pycurl.FOLLOWLOCATION, 0)

        if just_header:
            self.c.setopt(pycurl.NOBODY, 1)
        
        self.c.perform()
        rep = self.header if just_header else self.getResponse()

        if not follow_location:
            self.c.setopt(pycurl.FOLLOWLOCATION, 1)

        if just_header:
            self.c.setopt(pycurl.NOBODY, 0)

        self.c.setopt(pycurl.POSTFIELDS, "")
        self.lastEffectiveURL = self.c.getinfo(pycurl.EFFECTIVE_URL)

        if save_cookies:
            self.addCookies()

        try:
            self.code = self.verifyHeader()
        finally:
            self.rep.close()
            self.rep = None

        if decode:
            rep = self.decodeResponse(rep)

        return rep


    def verifyHeader(self):
        """Raise an exceptions on bad headers"""
        code = int(self.c.getinfo(pycurl.RESPONSE_CODE))
        if code in bad_headers:
            # 404 will NOT raise an exception
            raise BadHeader(code, self.getResponse())
        return code


    def checkHeader(self):
        """Check if header indicates failure"""
        return int(self.c.getinfo(pycurl.RESPONSE_CODE)) not in bad_headers


    def getResponse(self):
        """Retrieve response from string io"""
        if self.rep is None:
            return ""
        else:
            return self.rep.getvalue()


    def decodeResponse(self, rep):
        """Decode with correct encoding, relies on header"""
        header = self.header.splitlines()
        encoding = "utf8"  #: default encoding

        for line in header:
            line = line.lower().replace(" ", "")
            if not line.startswith("content-type:") or \
                    ("text" not in line and "application" not in line):
                continue

            none, delemiter, charset = line.rpartition("charset=")
            if delemiter:
                charset = charset.split(";")
                if charset:
                    encoding = charset[0]

        try:
            # self.log.debug("Decoded %s" % encoding )
            if codecs.lookup(encoding).name == 'utf-8' and rep.startswith(codecs.BOM_UTF8):
                encoding = 'utf-8-sig'

            decoder = codecs.getincrementaldecoder(encoding)("replace")
            rep = decoder.decode(rep, True)

            # TODO: html_unescape as default

        except LookupError:
            self.log.debug("No Decoder foung for %s" % encoding)

        except Exception:
            self.log.debug("Error when decoding string from %s." % encoding)

        return rep


    def write(self, buf):
        """Writes response"""
        if self.rep.tell() > 1000000 or self.abort:
            rep = self.getResponse()

            if self.abort:
                raise Abort

            with open("response.dump", "wb") as f:
                f.write(rep)
            raise Fail("Loaded url exceeded size limit")
        else:
            self.rep.write(buf)


    def writeHeader(self, buf):
        """Writes header"""
        self.header += buf


    def putHeader(self, name, value):
        self.headers.append("%s: %s" % (name, value))


    def clearHeaders(self):
        self.headers = []


    def close(self):
        """Cleanup, unusable after this"""
        if self.rep:
            self.rep.close()
        if hasattr(self, "cj"):
            del self.cj
        if hasattr(self, "c"):
            self.c.close()
            del self.c
