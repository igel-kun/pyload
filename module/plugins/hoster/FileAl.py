# -*- coding: utf-8 -*-

from module.plugins.internal.XFSHoster import XFSHoster
import re

class FileAl(XFSHoster):
    __name__    = "FileAl"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?file\.al/\w{12}'

    __description__ = """File.al hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]


    PLUGIN_DOMAIN = "file.al"
    LINK_PATTERN     = r'direct link.*?<a [^>]*href="(.+?)".*?>Click here to download'
    WAIT_PATTERN     = r'countdown.*?seconds.*?(\d+)'
    # "extend" the XFSHoster dict
    SEARCH_FLAGS     = dict(XFSHoster.SEARCH_FLAGS, **({'LINK': re.MULTILINE | re.DOTALL}))
    RECAPTCHA_PATTERN= r"g-recaptcha.*?sitekey=[\"']([^\"]*)"

    def setup(self):
        self.multiDL = self.premium
        self.resume_download = True
