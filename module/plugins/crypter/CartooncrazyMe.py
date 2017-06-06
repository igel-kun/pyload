# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleCrypter import SimpleCrypter


class CartooncrazyMe(SimpleCrypter):
    __name__    = "CartooncrazyMe"
    __type__    = "crypter"
    __version__ = "0.01"
    __status__  = "testing"
    # need cloudflare interaction!

    __pattern__ = r'https?://(?:www\.)?cartooncrazy\.me/.+'
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]


    __description__ = """Cartooncrazy.me decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", None)]

    OFFLINE_PATTERN = r'404 Page Not Found'
    IFRAME_PATTERN  = r'<div class="video_div".*?iframe src="(.*?)"'
    FILE_PATTERN    = r'jwplayer.*sources: \[.*?file: "(.*?)"'

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
        # step 1: get first HTML
        data = self.load(self.pyfile.url)
        # data should be some HTML with either an iframe or a jwplayer
        
        m = re.search(self.FILE_PATTERN, data, re.MULTILINE | re.DOTALL)
        if not m:
            m = re.search(self.IFRAME_PATTERN, data, re.MULTILINE | re.DOTALL)
        if not m:
            self.log_debug('error parsing response: %s' % data)

        url = m.group(1)
        return [url]


