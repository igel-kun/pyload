# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleHoster import SimpleHoster


class ARD(SimpleHoster):
    __name__    = "ARD"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?ardmediathek\.de'

    __description__ = """ARD hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]
    __config__ = [("activated", "bool", "Activated", True),
                  ("chk_filesize", "bool", "Check file size", True),
                  ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10),
                  ("max_quality", "int", "maximum width (in px) of video to download", 100000)]

    OFFLINE_PATTERN      = r'Seite nicht gefunden'
    NAME_PATTERN         = r'"clipTitle":"(?P<N>.*?)"'
    LINK_PATTERN         = r"http[^\"',]*mp4"

    def handle_free(self, pyfile):
        self.grab_info()
        best_quality = 0
        for i in re.finditer(self.LINK_PATTERN, self.data):
            m = re.search("/([0-9]*)-[^/]*.mp4", i.group(0))
            if m is not None:
                quality = int(m.group(1))
                # take the best quality below the given max quality
                if  quality <= self.config.get("max_quality") and quality > best_quality:
                    best_quality = quality
                    self.link = i.group(0)
