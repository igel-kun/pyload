# -*- coding: utf-8 -*-

import re

from module.plugins.internal.misc import eval_js_script
from module.plugins.internal.SimpleCrypter import SimpleCrypter


class WcryptCom(SimpleCrypter):
    __name__    = "WcryptCom"
    __type__    = "crypter"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?wcrypt\.com/.+'
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]


    __description__ = """Wcrypt.com decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "igelkun@myopera.com")]

    OFFLINE_PATTERN = r'404 Page Not Found'

    def process(self, pyfile):
        self.decrypt(pyfile)

    def decrypt(self, pyfile):
        self._prepare()
        self._preload()
        self.check_errors()

        # get the wcrypted links
        links = self.get_links()

        # add the links to the package containing ourself
        pid = pyfile.package().id
        self.log_debug('adding links: %s' % str(links))
        self.pyload.api.addFiles(pid, links)


    def get_links(self):
        printcmd = self.config.get('print_cmd', 'console.log')
        # step 1: get first HTML
        data = self.load(self.pyfile.url)
        # data should be some HTML with a coded javascript that we'll extract
        
        # step 2: interprete the javascript code
        m = re.search('<script language="javascript"[^>]*>(.*?)</script>', data)

        if not m:
            self.log_debug('error parsing response: %s' % data)

        js_code = re.sub('eval', printcmd, m.group(1))
        data = eval_js_script(js_code)
        # data should now be another javascript that basically unescapes a string called "_escape"

        # step 3: run the second javascript code
        m = re.search('var[^=a-zA-Z]*=(.*?);', data)
        
        if not m:
            self.log_debug('error parsing script: %s' % data)

        js_code2 = m.group(1)
        data = eval_js_script(js_code2)
        # data should now be the HTML code of an iframe pointing to "/i.php[...]"

        # step 4: get the HTML from the <iframe>
        m = re.search('src="(.*?)"', data)

        if not m:
            self.log_debug('error parsing iframe URL from %s' % data)

        iframe_url = m.group(1)

        # NOTE: it is necessary to provide the correct cookies AND referer here! wcrypt will check
        self.req.http.lastURL = self.pyfile.url
        self.log_debug('referer is %s' % self.req.http.lastURL)
        data = self.load('http://wcrypt.com%s' % iframe_url, cookies = True, ref = True)
        # self.log_debug('final page: %s' % data)
        # data should now be an HTML document containing another javasctipt that just sets window.top.location.href to the final URL

        # step 5: get the url from the new document
        m = re.search('href\s*=\s*[\'"](.*?)[\'"]', data)

        if not m:
            self.log_debug('error parsing iframe content: %s' % data)

        url = m.group(1)
        return [url]


