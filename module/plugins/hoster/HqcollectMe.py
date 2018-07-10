# -*- coding: utf-8 -*-

import re
from module.plugins.internal.SimpleHoster import SimpleHoster


class HqcollectMe(SimpleHoster):
    __name__    = "HqcollectMe"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?hqcollect\.me/(?:pack|movies)/(?P<pname>[^/]+)/(?P<item>.+)'
    __description__ = """Hqcollect.me hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]

    LINK_PATTERN = r'<source src="([^"]*?)" type="video'
    PREMIUM_ONLY_PATTERN = r'(?:This title is not available to watch instantly but|This page not available anymore for public access, but)'
    DISPOSITION = False
    INFO_PATTERN = r'<meta name="description" content="(?P<N>.*?) \((?P<S>[\d.]) (?P<U>[KMG]?B)\)'
    ERROR_PATTERN = r'Your limit for browsing videos was reached'

