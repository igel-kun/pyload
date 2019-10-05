# -*- coding: utf-8 -*-

from ..accounts.Keep2ShareCc import Keep2ShareCc


class FileboomMe(Keep2ShareCc):
    __name__ = "FileboomMe"
    __type__ = "account"
    __version__ = "0.01"
    __status__ = "testing"

    __description__ = """Fileboom.me hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("igel", None)]

    API_URL = 'https://www.fileboom.me/api/v2/'



