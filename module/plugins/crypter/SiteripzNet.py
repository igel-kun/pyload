# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleCrypter import SimpleCrypter
from subprocess import Popen, PIPE, STDOUT
from tempfile import NamedTemporaryFile

class SiteripzNet(SimpleCrypter):
    __name__    = "SiteripzNet"
    __type__    = "crypter"
    __version__ = "0.01"

    __pattern__ = r'http://(?:www\.)?siteripz\.net/.*'
    __description__ = """SiteripZ.net decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = []

    LINK_PATTERN = r'iframe.*src="(http://(?:w{3}\.)?[^"]*)"'

    OFFLINE_PATTERN = r'File Not Found'

    def get_links(self):
        tmpfile = NamedTemporaryFile(suffix='.js',delete=False)
        print 'saving to %s' % tmpfile.name

        # change the script as to print the URL
        m = re.search('<script.*?>(.*?)</script>',self.html, re.MULTILINE | re.DOTALL)
        rawscript = m.group(1)
        newscript = re.sub('document.*(base64_decode.*?)\+[\w\[\]]+;','print(\1);',rawscript)

        # call spidermonkey to get the source URL
        tmpfile.write(newscript.encode('utf-8'))
        cmd = "/usr/local/bin/smjs %s" % tmpfile.name
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        link = p.stdout.read()
        tmpfile.close()

        print 'encrypted HTML: %s' % self.html
        print 'link: %s' % link
        return link

