# -*- coding: utf-8 -*-

from ..internal.XFSAccount import XFSAccount


class StreaminTo(XFSAccount):
    __name__ = "StreaminTo"
    __type__ = "account"
    __version__ = "0.07"
    __status__ = "testing"

    __description__ = """Streamin.to account plugin"""
    __license__ = "GPLv3"
    __authors__ = [("igel", None)]

    PLUGIN_DOMAIN = "streamin.to"
