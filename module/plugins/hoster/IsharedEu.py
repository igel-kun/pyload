# -*- coding: utf-8 -*-
from module.plugins.hoster.XFileSharing import XFileSharing


class IsharedEu(XFileSharing):
    __name__ = "IsharedEu"
    __type__ = "hoster"
    __pattern__ = r"http://(?:\w*\.)*ishared\.eu/(?:embed/)?([^?]*)"
    __version__ = "0.01"
    __description__ = """IsharedEu plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    DIRECT_LINK_PATTERN = r'var zzzz = "([^"]*)";'

    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1

