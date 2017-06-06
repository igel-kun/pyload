# -*- coding: utf-8 -*-

from module.plugins.internal.XFSHoster import XFSHoster


class FileAl(XFSHoster):
    __name__    = "FileAl"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'http://(?:www\.)?file\.al/\w{12}'

    __description__ = """File.al hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]


    PLUGIN_DOMAIN = "file.al"
    LINK_PATTERN     = r'<a href="(.+?)".*?>Click here to download'

