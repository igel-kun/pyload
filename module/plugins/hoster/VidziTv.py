# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class VidziTv(JWPlayerBased):
    __name__ = "VidziTv"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"http://(?:\w*\.)*vidzi\.tv/(?:embed|\w{12})"
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """VidziTv plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    JW_PATTERN = r'<script .*?jwplayer.*?setup\({(.*?)</script>'
    JW_LINK_PATTERN = r"{ *file *: *[\"']([^\"']*)[\"']}\]"


