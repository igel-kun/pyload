# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class StreaminTo(JWPlayerBased):
    __name__ = "StreaminTo"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"http://(?:\w*\.)*streamin\.to/\w{12}"
    __description__ = """StreaminTo plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    JW_LINK_PATTERN = r"modes:.*?config:\s*{\s*file:\s*[\"'](.*?)[\"'].*download"


