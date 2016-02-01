# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleCrypter import SimpleCrypter
from urlparse import urljoin

class KoukniCzCrypt(SimpleCrypter):
    __name__    = "KoukniCzCrypt"
    __type__    = "crypter"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?koukni\.cz/hledej'

    __description__ = """Koukni.cz decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]


    #LINK_PATTERN = r'href="https?://(?:www\.)?koukni\.cz/hledej\?"'
    NAME_PATTERN = r'<[tT]itle>Watch (?P<N>.+?)<'
    PAGES_PATTERN = r'yes, there are pages'

    LINK_FREE_PATTERN = r'<div class="mosaic-block bar">.*?href="(/\d+)"'

    # if this matches, it's the last page
    LAST_PAGE_PATTERN = r'\((?:&gt;|>)\)\s*-\s*\((?:&gt;&gt;|>>)\)'
    # group(1) of this contains the URL of the next page
    NEXT_PAGE_PATTERN = r'<a href="([^"]*)">\((?:&gt;|>)\)</a>'
    NAME_PATTERN = r'name="hledej".*value="([^"]*)"'

    # as we don't know how many pages we have, we have to overwrite handle_pages
    def handle_pages(self, pyfile):
        self.log_debug('handling pages...')
        while True:
            match = re.search(self.LAST_PAGE_PATTERN, self.data)
            if match is not None:
                self.log_debug('this was the last page')
                break

            next_page = re.search(self.NEXT_PAGE_PATTERN, self.data)
            if next_page is None:
                self.fail(_('Something is wrong: this is not the last page but we cannot find the next page!'))

            self.log_debug("loading next page of links")
            next_url = urljoin(pyfile.url, next_page.group(1))
            self.data = self.load(next_url)
            
            # get_links is already incremental, no need to extend links again
            self.get_links(pyfile)

    # seriously, this handle_direct in crypters is the worst idea ever!
    def handle_direct(self, pyfile):
        self.links = []

