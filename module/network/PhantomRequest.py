#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: igel
"""

import subprocess
import os 
import tempfile

from urllib import quote, urlencode
from logging import getLogger

from HTTPRequest import myquote, myurlencode
from ..common.JsEngine import call_external

# remove this as soon as plusing/internal/Plugin.py is fixed!
import pycurl

class PhantomRequest():

    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
    FAKE_HEADER = {'code': 200, 'Content-Type': 'text/html'}
    # the headless browser needs to be told to work headlessly, otherwise it'll crash...
    PHANTOM_ENV = {'QT_QPA_PLATFORM': 'offscreen'}

    #TODO: add external cookies!

    def __init__(self, cookies=None, options=None):
        # for some reason, plugins/internal/Plugin.py has to play with the pycurl object, so we have to have an aliby one
        self.c = pycurl.Curl()

        self.cj = cookies
        if cookies:
            self.cfile = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            if type(cookies) != bool:
                self.cfile.write(str(cookies.getCookies())) #cookiejar
            self.cfile.close()
        else:
            self.cfile = None

        # fake a header
        self.code = 200
        self.header = ''.join(["%s:%s\n" % (k,v) for k,v in self.FAKE_HEADER.iteritems()])

        self.rep = ""
        self.headers = None
        self.lastURL = None
        self.lastEffectiveURL = None
        self.log = getLogger("log")

        if options and 'proxies' in options:
            self.proxy = options["proxies"]
        else:
            self.proxy = None


    def __del__(self):
        if self.cfile:
            #os.remove(self.cfile.name)
            pass

    def addCookies(self):
        """ put cookies from cfile to cj """
        #self.cfile = open(self.cfile.name, 'r')
        pass

    def getCookies(self):
        """ add cookies from cj to cfile """
        pass

    def clearCookies(self):
        f = open(self.cfile.name, 'w')
        f.close()

    def verifyHeader(self):
        """ raise an exceptions on bad headers """
        return 200

    def checkHeader(self):
        """ check if header indicates failure"""
        return True

    def getResponse(self):
        """ retrieve response from string io """
        return self.rep

    def write(self, buf):
        """ writes response """
        self.rep += buf

    def writeHeader(self, buf):
        """ writes header """
        self.header += buf

    def putHeader(self, name, value):
        self.headers.append("%s: %s" % (name, value))

    def clearHeaders(self):
        self.headers = []

    def close(self):
        """ cleanup, unusable after this """
        pass

    def load(self, url, get={}, post={}, referer=True, cookies=True, just_header=False, multipart=False, decode=False):
       
        url = myquote(url)
        if get:
            get = urlencode(get)
            url = "%s?%s" % (url, get)


        if just_header:
            print 'just_header is not implemented for phantomJS - for now, we just return a standard header'
            # TODO: implement me
            return self.FAKE_HEADER
            

        script = tempfile.NamedTemporaryFile(suffix='.js', delete=False)
        js_init = "var page = require('webpage').create();"
        js_callback_fn = "function(status) { if(status != 'success') { console.log('FAIL'); } else { console.log(page.content); }; phantom.exit(); }";
        js_settings = "page.settings.userAgent = '" + self.USER_AGENT + "';"

        # settings
        js_settings += 'page.customHeaders = {'
        if referer and self.lastURL:
            if self.headers:
                self.headers['Referer'] = self.lastURL
            else:
                js_settings += '"Referer" : "' + self.lastURL + '"'
        if self.headers:
            for key, val in self.headers:
                js_settings += ' "%s" : "%s",' % (key, val)
            js_settings = js_settings[:-1]
        js_settings += '};'

        # prepare the call to open the website
        js_open_call = "page.open('" + url + "', "
        if post:
            if type(post) == unicode:
                post = str(post) #unicode not allowed
            elif type(post) == str:
                pass
            else:
                post = myurlencode(post)
            js_open_call += "'POST', '" + post + "', "

        js_open_call += js_callback_fn + ");";

        script.write(js_init + js_settings + js_open_call)
        script.close()

        # prepare command-line arguments
        phantom_args = ['phantomjs', '--load-images=false']
        if self.proxy:
            phantom_args += ['--proxy=%s:%s' % (self.proxy['address'], self.proxy['port'])]
            phantom_args += ['--proxy-type=' + self.proxy['type']]
            if self.proxy['username']:
                phantom_args += ['--proxy-auth=%s:%s' % (self.proxy['username'], self.proxy['password'])]

        if self.cfile:
            phantom_args += ['--cookies-file=' + self.cfile.name]
        phantom_args += [script.name]

        self.rep = call_external(phantom_args, extra_env = self.PHANTOM_ENV)
        #os.remove(script.name)

        return self.rep



if __name__ == "__main__":
    from CookieJar import CookieJar
    p = PhantomRequest(cookies = CookieJar(None))
    #    print p.load('http://www.html-kit.com/tools/cookietester/', post={'cn':'cookiename', 'cv':'my cookie smells yummy'})
    print p.load('http://airbnb.com')
