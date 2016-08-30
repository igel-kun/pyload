# -*- coding: utf-8 -*-


import re
from module.plugins.internal.misc import parse_size
from module.plugins.internal.SimpleHoster import SimpleHoster


class ThevideoMe(SimpleHoster):
    __name__ = "ThevideoMe"
    __type__ = "hoster"
    __version__ = "0.03"
    __status__  = "testing"

    __pattern__ = r'(?:https?://)?(?:\w*\.)*thevideo\.me/(?:download/|embed-)?(?P<id>\w{12})'
    __description__ = """thevideo.me plugin"""
    __license__     = "GPLv3"
    __authors__ = [("igel", "")]

    BASE_URL = 'http://thevideo.me/'
    FORM_PATTERN = r'<form id="veriform".*?</form>'
    VERSION_PATTERN = r"onclick=\"download_video\('\w*','(?P<short>.)','(?P<long>[^']*)'\)\">(?P<qual>[^<]*)</a>.*?(?P<resx>\d+)[0-9x]*,\s*(?P<size>[^<]*)<"
    LINK_PATTERN = r'<a href="([^"]*)" name="dl" id="btn_download".*Download'
    NAME_PATTERN = r'<h1[^>]*>Download\w*\s(?P<N>[^<]*)<'
    OFFLINE_PATTERN = r'not\s*\w*\sfound'
    DL_ORIG_PATTERN = r'name="op".*value="download_orig"'

    URL_REPLACEMENTS = [(__pattern__ + ".*", BASE_URL + r'download/\g<id>')]

    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1
        self.resumeDownload = True


    def handle_free(self, pyfile):
        file_id = re.search(self.__pattern__, pyfile.url).group('id')
        self.data = self.load(self.BASE_URL + 'cgi-bin/index_dl.cgi?op=get_vid_versions&file_code=%s' % file_id)

        # get the best quality version
        available_versions = re.findall(self.VERSION_PATTERN, self.data)
        urls = dict()
        sizes = dict()
        for short_url,long_url,qual,resx,size in available_versions:
            urls[resx] = self.BASE_URL + 'download/' + file_id + '/' + short_url + '/' + long_url
            sizes[resx] = size
        
        self.log_debug('versions: %s' % str(urls))

        # get best quality page
        largest_x_res = max(urls, key=int)
        url = urls[largest_x_res]
        self.info['size'] = parse_size(sizes[largest_x_res])
        self.data = self.load(url)

        # sometimes, we're not getting directly to the video, but to a page with a "Download Original Video" button
        while re.search(self.DL_ORIG_PATTERN, self.data) is not None:
            # in this case, press the button to get to the site containing the link
            action, inputs = self.parse_html_form('F1')
            self.log_debug('parsed inputs: %s' % str(inputs))
            self.data = self.load(url, post=inputs)

        # get file from there
        self.link = re.search(self.LINK_PATTERN, self.data).group(1)


