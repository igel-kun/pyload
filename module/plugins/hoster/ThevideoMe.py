# -*- coding: utf-8 -*-
from module.plugins.internal.SimpleHoster import SimpleHoster
from module.plugins.internal.XFSHoster import _post_parameters

import re

class ThevideoMe(SimpleHoster):
    __name__ = "ThevideoMe"
    __type__ = "hoster"
    __version__ = "0.02"
    __status__  = "testing"

    __config__  = [("activated"   , "bool", "Activated"                                        , True)]
    __pattern__ = r'(?:https?://)?(?:\w*\.)*thevideo\.me/(?:download/|embed-)?(?P<id>\w{12})'
    __description__ = """thevideo.me plugin"""
    __license__     = "GPLv3"
    __authors__ = [("igel", "")]

    BASE_URL = 'http://thevideo.me/'
    FORM_PATTERN = r'<form id="veriform".*?</form>'
    VERSION_PATTERN = r"onclick=\"download_video\('\w*','(?P<short>.)','(?P<long>[^']*)'\)\">(?P<qual>[^<]*)</a>.*?(?P<resx>\d+)[0-9x]*,\s*(?P<size>\d*)[. ]"
    LINK_PATTERN = r'<a href="([^"]*)" name="dl" id="btn_download".*Download'
    NAME_PATTERN = r'<h1[^>]*>Download ([^<]*)<'
    OFFLINE_PATTERN = r'not\s*\w*\sfound'
    DL_ORIG_PATTERN = r'name="op".*value="download_orig"'

    URL_REPLACEMENTS = [(__pattern__ + ".*", BASE_URL + r'download/\g<id>')]

    def handle_free(self, pyfile):
        file_id = re.search(self.__pattern__, pyfile.url).group('id')
        self.data = self.load(self.BASE_URL + 'cgi-bin/index_dl.cgi?op=get_vid_versions&file_code=%s' % file_id)

        # get the best quality version
        available_versions = re.findall(self.VERSION_PATTERN, self.data)
        ver = dict()
        for short_url,long_url,qual,resx,size in available_versions:
            ver[resx] = self.BASE_URL + 'download/' + file_id + '/' + short_url + '/' + long_url
        
        self.log_debug('versions: %s' % str(ver))

        # get best quality page
        url = ver[max(ver, key=int)]
        self.data = self.load(url)

        # sometimes, we're not getting directly to the video, but to a page with a "Download Original Video" button
        m = re.search(self.DL_ORIG_PATTERN, self.data)
        if m is not None:
            # in this case, press the button to get to the site containing the link
            self.data = self.load(url, post=self._post_parameters())

        # get file from there
        self.link = re.search(self.LINK_PATTERN, self.data).group(1)


