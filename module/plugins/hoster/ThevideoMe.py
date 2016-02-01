# -*- coding: utf-8 -*-
from module.plugins.internal.SimpleHoster import SimpleHoster

import re

class ThevideoMe(SimpleHoster):
    __name__ = "ThevideoMe"
    __type__ = "hoster"
    __version__ = "0.02"
    __status__  = "testing"

    __config__  = [("activated"   , "bool", "Activated"                                        , True)]
    __pattern__ = r'(?:https?://)?(?:\w*\.)*thevideo\.me/(?:download/)?(?P<id>\w{12})'
    __description__ = """thevideo.me plugin"""
    __license__     = "GPLv3"
    __authors__ = [("igel", "")]

    BASE_URL = 'http://thevideo.me/'
    FORM_PATTERN = r'<form id="veriform".*?</form>'
    VERSION_PATTERN = r"onclick=\"download_video\('\w*','(?P<short>.)','(?P<long>[^']*)'\)\">(?P<qual>[^<]*)</a>.*?\s(?P<size>\d*)[. ]"
    LINK_PATTERN = r'<a href="([^"]*)" name="dl" id="btn_download".*Download'

    def handle_free(self, pyfile):
        file_id = re.search(self.__pattern__, pyfile.url).group('id')
        self.data = self.load(self.BASE_URL + 'cgi-bin/index_dl.cgi?op=get_vid_versions&file_code=%s' % file_id)

        # get the best quality version
        available_versions = re.findall(self.VERSION_PATTERN, self.data)
        ver = dict()
        for short_url,long_url,qual,size in available_versions:
            ver[size] = self.BASE_URL + 'download/' + file_id + '/' + short_url + '/' + long_url
        
        self.log_debug('versions: %s' % str(ver))

        # get best quality page
        self.data = self.load(ver[max(ver, key=int)])

        # get file from there
        self.link = re.search(self.LINK_PATTERN, self.data).group(1)


