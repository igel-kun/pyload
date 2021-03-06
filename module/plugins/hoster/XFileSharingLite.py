# -*- coding: utf-8 -*-
from module.plugins.hoster.XFileSharing import XFileSharing


class XFileSharingLite(XFileSharing):
    __name__ = "XFileSharingLite"
    __type__ = "hoster"
    __pattern__ = r"http://(?:\w*\.)*(?P<DOMAIN>played\.to|faststream\.in)/\w{12}"
    __version__ = "0.01"
    __description__ = """XFileSharingLite plugin"""
    __license__ = "GPLv3"
    __authors__ = [("igel", None)]

    WAIT_TIME = r'countdown[^0-9]*(\d+)'
    # if called without DOTALL, we need this:
    #LINK_PATTERN = r'jwplayer(?:.|\n)*?file: "([^"]*)"'
    # with DOTALL, do this:
    LINK_PATTERN = "jwplayer.*?['\"]?file['\"]?\s*: ['\"]([^'\"]*)['\"]"

    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1
        self.resume_download = True

