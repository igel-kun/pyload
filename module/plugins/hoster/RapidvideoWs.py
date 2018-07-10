# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class RapidvideoWs(JWPlayerBased):
    __name__ = "RapidvideoWs"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"http://(?:\w*\.)*rapidvideo\.ws/(?:embed|\w{12})"
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """RapidvideoWs plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    #JW_PATTERN = r"<script .*?javascript'>(eval.*?)(?:</script>|$)"
    #JW_LINK_PATTERN = r"{file:[\"']([^\"']*)[\"']"


