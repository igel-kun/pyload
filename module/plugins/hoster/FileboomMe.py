# -*- coding: utf-8 -*-


from Keep2ShareCc import Keep2ShareCc


class FileboomMe(Keep2ShareCc):
    __name__ = "FileboomMe"
    __type__ = "hoster"
    __version__ = "0.09"
    __status__ = "testing"

    __pattern__ = r'https?://f(?:ile)?boom\.me/file/(?P<ID>\w+)'
    __config__ = [("activated", "bool", "Activated", True),
                  ("use_premium", "bool", "Use premium account if available", True),
                  ("fallback", "bool",
                   "Fallback to free download if premium fails", True),
                  ("chk_filesize", "bool", "Check file size", True),
                  ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10)]

    __description__ = """Fileboom.me hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("GammaC0de", None),
                   ("igel", None)]

    OFFLINE_PATTERN = r'>This file is no longer available'
    
    API_URL = 'https://fileboom.me/api/v2/'
    SLOW_ID_PATTERN = r'data-slow-id="(.+?)"'
    URL_REPLACEMENTS = []

    

