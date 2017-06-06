# -*- coding: utf-8 -*-

from module.plugins.hoster.Keep2ShareCc import Keep2ShareCc

class TezfilesCom(Keep2ShareCc):
    __name__    = "TezfilesCom"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?tezfiles\.com/file/(?P<ID>\w+)'

    __description__ = """Tezfiles.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]


