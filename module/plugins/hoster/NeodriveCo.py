# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class NeodriveCo(JWPlayerBased):
    __name__ = "NeodriveCo"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r'(?:https?://)?(?:\w*\.)*neodrive\.co/(?:share/file/|embed/)?(?P<id>\w*)'
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """NeodriveCo plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    BASE_URL = 'http://neodrive.co/'
    NAME_PATTERN = r'<div\s*id="title"><a/*?>(?P<N>.*?)</a>'
    JW_PATTERN = r"^\s*(eval.*?)\n"
    JW_LINK_PATTERN = r"var vurl=[\"'](.*?)[\"'];"

    URL_REPLACEMENTS = [(__pattern__ + ".*", BASE_URL + r'embed/\g<id>')]

