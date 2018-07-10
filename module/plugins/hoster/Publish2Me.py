# -*- coding: utf-8 -*-


from Keep2ShareCc import Keep2ShareCc


class Publish2Me(Keep2ShareCc):
    __name__ = "Publish2Me"
    __type__ = "hoster"
    __version__ = "0.08"
    __status__ = "testing"

    __pattern__ = r'https?://publish2\.me/file/(?P<ID>\w+)'
    __config__ = [("activated", "bool", "Activated", True),
                  ("use_premium", "bool", "Use premium account if available", True),
                  ("fallback", "bool",
                   "Fallback to free download if premium fails", True),
                  ("chk_filesize", "bool", "Check file size", True),
                  ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10)]

    __description__ = """Publish2.me hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("igel", None)]

    OFFLINE_PATTERN = r'>This file is no longer available'
    PREMIUM_ONLY_PATTERN = r'This file is available.*only for premium members'
    WAIT_PATTERN = r'<div class="tik-tak">([\d:]+)'
    
    API_URL = 'https://publish2.me/api/v2/'
    SLOW_ID_PATTERN = r'data-slow-id="(\w+)"'
    

