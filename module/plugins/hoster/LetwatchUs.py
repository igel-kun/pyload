# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class LetwatchUs(JWPlayerBased):
    __name__ = "LetwatchUs"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"http://(?:\w*\.)*letwatch\.us/(?:embed|\w{12})"
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """LetwatchUs plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    #JW_PATTERN = r"<script .*?javascript'>(eval.*?)(?:</script>|$)"
    JW_LINK_PATTERN = r"{file:[\"']([^\"']*)[\"']"


