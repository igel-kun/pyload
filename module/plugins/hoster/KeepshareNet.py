# -*- coding: utf-8 -*-

from module.plugins.internal.XFSHoster import XFSHoster


class KeepshareNet(XFSHoster):
    __name__    = "KeepshareNet"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?keepshare\.net/\w{12}'

    __description__ = """Keepshare.net hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]


    PLUGIN_DOMAIN = "keepshare.net"
    WAIT_PATTERN  = "You have to wait (.*?) till next download"



