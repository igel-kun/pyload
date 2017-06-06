# -*- coding: utf-8 -*-


from module.plugins.internal.SimpleHoster import SimpleHoster

class SockshareCom(SimpleHoster):
    __name__ = "SockshareCom"
    __type__ = "hoster"
    __pattern__ = r'http://(?:www\.)?sockshare\.(?:net|com)/(mobile/)?(file|embed)/(?P<ID>[A-Z0-9]+)'
    __version__ = "0.12"
    __config__ = []  # @TODO: Remove in 0.4.10
    __description__ = """Sockshare.Net"""
    __license__ = "GPLv3"
    __authors__ = [("jeix", "jeix@hasnomail.de"),
                   ("stickell", "l.stickell@yahoo.it"),
                   ("Walter Purcaro", "vuolter@gmail.com")]

    FILE_URL_REPLACEMENTS = [(__pattern__, r'http://www.sockshare.net/file/\g<ID>')]
    HOSTER_NAME = "sockshare.net"


