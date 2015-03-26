# -*- coding: utf-8 -*-

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class TwoSharedCom(SimpleHoster):
    __name__    = "TwoSharedCom"
    __type__    = "hoster"
    __version__ = "0.13"

    __pattern__ = r'http://(?:www\.)?2shared\.com/(account/)?(download|get|file|document|photo|video|audio)/.+'

    __description__ = """2Shared.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg", "zoidberg@mujmail.cz")]


    NAME_PATTERN    = r'<h1>(?P<N>.*)</h1>'
    SIZE_PATTERN    = r'<span class="dtitle">File size:</span>\s*(?P<S>[\d.,]+) (?P<U>[\w^_]+)'
    OFFLINE_PATTERN = r'The file link that you requested is not valid\.|This file was deleted\.'

    LINK_FREE_PATTERN = r'window.location =\'(.+?)\';'


    def setup(self):
        self.resumeDownload = True
        self.multiDL        = True
