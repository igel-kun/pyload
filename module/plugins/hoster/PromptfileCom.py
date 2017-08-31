# -*- coding: utf-8 -*-

from ..internal.DeadHoster import DeadHoster


class PromptfileCom(DeadHoster):
    __name__ = "PromptfileCom"
    __type__ = "hoster"
    __version__ = "0.19"
    __status__ = "stable"

    __pattern__ = r'https?://(?:www\.)?promptfile\.com/'
    __description__ = """Promptfile.com hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("igel", "igelkun@myopera.com"),
                   ("ondrej", "git@ondrej.it")]


