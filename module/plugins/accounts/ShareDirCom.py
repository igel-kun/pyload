# -*- coding: utf-8 -*-

import re
import time

from module.plugins.internal.Account import Account
from module.plugins.internal.misc import parse_size


class ShareDirCom(Account):
    __name__    = "ShareDirCom"
    __type__    = "account"
    __version__ = "0.01"
    __status__  = "testing"

    __description__ = """ShareDir account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", None)]


    VALID_UNTIL_PATTERN  = r'' # TODO once I get my hands on a premium account :)
    TRAFFIC_LEFT_PATTERN = r'You have .*? \((.*?)\) traffic left for today'
    LOGIN_FAIL_PATTERN = r'Invalid username'
    ACCOUNT_TYPE_PATTERN = r'Account type: <[^>]*>(\w+)'
    MAX_SIZE = 150 * 1024 * 1024 # currently, they allow 500MB daily traffic

    def grab_info(self, user, password, data):
        html = self.load("https://sharedir.com/panel.html")
        premium = True if re.search(self.ACCOUNT_TYPE_PATTERN, html).group(1) == "Premium" else False;
        return {'maxtraffic': -1 if premium else self.MAX_SIZE,
                'trafficleft': parse_size(re.search(self.TRAFFIC_LEFT_PATTERN, html).group(1)) / 1024, #@TODO: Remove `/ 1024` in 0.4.10
                'premium': premium }


    def signin(self, user, password, data):
        html = self.load("https://sharedir.com/login.html", post={'username': user, 'password': password, 'login_submit': ""})
        if self.LOGIN_FAIL_PATTERN in html:
            self.fail_login()

        
