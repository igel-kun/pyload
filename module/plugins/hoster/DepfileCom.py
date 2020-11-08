# -*- coding: utf-8 -*-


from module.plugins.internal.DeadHoster import DeadHoster


class DepfileCom(DeadHoster):
    __name__ = "DepfileCom"
    __type__ = "hoster"
    __version__ = "0.02"
    __status__  = "testing"

    __pattern__ = r'(?:https?://)?(?:www\.)*depfile\.(?:com|us)/'
    __description__ = """depfile.com plugin"""
    __license__     = "GPLv3"
    __authors__ = [("igel", "")]


