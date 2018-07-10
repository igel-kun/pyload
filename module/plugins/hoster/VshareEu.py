# -*- coding: utf-8 -*-

from module.plugins.hoster.JWPlayerBased import JWPlayerBased


class VshareEu(JWPlayerBased):
    __name__ = "VshareEu"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"http://(?:\w*\.)*vshare\.eu/(?:embed|\w{12})"
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """VshareEu plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    #JW_PATTERN = r"<script .*?javascript'>(eval.*?)(?:</script>|$)"
    JW_LINK_PATTERN = r"\.setup.*?file:\s*[\"'](.*?)[\"']"


