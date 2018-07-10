# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class FlashxTv(JWPlayerBased):
    __name__ = "FlashxTv"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"http://(?:\w*\.)*flashx\.tv/(?:embed|\w{12})"
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """FlashxTv plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    #JW_PATTERN = r"<script .*?javascript'>(eval.*?)(?:</script>|$)"
    #JW_LINK_PATTERN = r"{file:[\"']([^\"']*)[\"']"


