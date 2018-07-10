# -*- coding: utf-8 -*-

from ..internal.DeadHoster import DeadHoster


class NosvideoCom(DeadHoster):
    __name__ = "NosvideoCom"
    __type__ = "hoster"
    __version__ = "0.02"
    __status__ = "stable"

    __pattern__ = r'(?:https?://)?(?:\w*\.)?nosvideo\.com/'
    __config__ = []  # @TODO: Remove in 0.4.10

    __description__ = """Nosvideo.com hoster plugin"""
    __license__ = "GPLv3"
