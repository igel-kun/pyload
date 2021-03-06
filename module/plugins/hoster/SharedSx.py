# -*- coding: utf-8 -*-

from module.plugins.hoster.XFileSharing import XFileSharing


class SharedSx(XFileSharing):
    __name__ = "SharedSx"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"https?://(?:\w*\.)*(?P<DOMAIN>shared\.sx)/"
    __description__ = """shared.sx plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    # FORM_PATTERN = r'<form\s*method="post">(.*?>Continue to file<.*?)</form>'
    FORM_PATTERN = 'method'
    INFO_PATTERN = '<h1 data-hash.*?>\w* (?P<N>[^<]+)<strong>\((?P<S>[\d.]+) (?P<U>\w+)\)</strong>'
    WAIT_TIME = r'var countdownNum = (\d+)'
    # if called without DOTALL, we need this:
    #DIRECT_LINK_PATTERN = r'jwplayer(?:.|\n)*?file: "([^"]*)"'
    LINK_PATTERN = r'data-url="([^"]*)"'

    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1

