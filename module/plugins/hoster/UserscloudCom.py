# -*- coding: utf-8 -*-

from module.plugins.internal.XFSHoster import XFSHoster


class UserscloudCom(XFSHoster):
    __name__    = "UserscloudCom"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?userscloud\.com/\w{12}'

    __description__ = """Userscloud.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]


    PLUGIN_DOMAIN = "userscloud.com"
    LINK_PATTERN  = r'^<a href="http(.*?)".*window'

