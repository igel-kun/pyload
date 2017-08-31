# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleCrypter import SimpleCrypter


class TreasureenCom(SimpleCrypter):
    __name__    = "TreasureenCom"
    __type__    = "crypter"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?treasureen\.com'

    __description__ = """Treasureen decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = []


    OFFLINE_PATTERN = r'Page Not Found'
    TEMP_OFFLINE_PATTERN = None
    LINK_PATTERN = r'class="themeform" href="(http.*?)"'

    def process(self, pyfile):
        self.decrypt(pyfile)

    def decrypt(self, pyfile):
        self._prepare()
        self._preload()
        self.check_errors()

        links = self.get_links()

        # add the links to the package containing ourself
        pid = pyfile.package().id
        self.log_debug('adding links: %s' % str(links))
        self.pyload.api.addFiles(pid, links)


