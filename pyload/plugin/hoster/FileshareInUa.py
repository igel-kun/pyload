# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class FileshareInUa(DeadHoster):
    __name__    = "FileshareInUa"
    __type__    = "hoster"
    __version__ = "0.02"

    __pattern__ = r'https?://(?:www\.)?fileshare\.in\.ua/\w{7}'

    __description__ = """Fileshare.in.ua hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("fwannmacher", "felipe@warhammerproject.com")]
