# -*- coding: utf-8 -*-
#
# ATTENTION: if you cannot see the interactive captcha (on firefox), make sure to activate/install X-Frame-Options Header:
# https://addons.mozilla.org/en-US/firefox/addon/ignore-x-frame-options-header/

from module.plugins.internal.XFSHoster import XFSHoster
import re

class FileAl(XFSHoster):
    __name__    = "FileAl"
    __type__    = "hoster"
    __version__ = "0.02"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?file\.al/\w{12}'

    __description__ = """File.al hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]

    PLUGIN_DOMAIN = "file.al"
    LINK_PATTERN     = r'direct link.*?<a [^>]*href="(.+?)".*?>Click here to download', re.MULTILINE | re.DOTALL
    WAIT_PATTERN     = r'countdown.*?seconds.*?(\d+)'
    INFO_PATTERN = r'You have requested.*https?://[^<]*?(?P<N>[^/<]*)</.*?\((?P<S>[0-9.]* [A-Z]?B)'
    RECAPTCHA_PATTERN = r"g-recaptcha.*?sitekey=[\"']([^\"]*)"
    PREMIUM_ONLY_PATTERN  = r'(?:[Pp]remium Users only|can download files up to.*only)'
    DL_LIMIT_PATTERN = r'You have reached the download-limit:[^<]*'

    #LOCAL_LOCATION = r'check_ip'
    #PRE_CAPTCHA_PATTERN = r"confirm that you're not a robot"

    def setup(self):
        self.multiDL = self.premium
        self.resume_download = self.premium

