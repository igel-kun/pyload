# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleCrypter import SimpleCrypter


class Seriescr(SimpleCrypter):
    __name__    = "Seriescr"
    __type__    = "crypter"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?seriescr\.com'

    __description__ = """SeriesCR decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = []


    OFFLINE_PATTERN = r'Page Not Found'
    TEMP_OFFLINE_PATTERN = None
    # a preprocess pattern limits the search scope for the LINK_PATTERN
    PREPROCESS_PATTERN = r'<div class="entry">.*<div class="widebanner">'
    LINK_PATTERN = r'<a href="(http.*?)">'

    def process(self, pyfile):
        self.decrypt(pyfile)

    def preprocess(self):
        self.data = re.search(self.PREPROCESS_PATTERN, self.data, re.MULTILINE | re.DOTALL).groups(0)

    def decrypt(self, pyfile):
        self._prepare()
        self._preload()
        self.check_errors()
        self.preprocess()
        links = self.get_links()

