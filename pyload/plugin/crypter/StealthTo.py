# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class StealthTo(DeadCrypter):
    __name__    = "StealthTo"
    __type__    = "crypter"
    __version__ = "0.20"

    __pattern__ = r'http://(?:www\.)?stealth\.to/folder/.+'
    __config__  = []

    __description__ = """Stealth.to decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("spoob", "spoob@pyload.org")]
