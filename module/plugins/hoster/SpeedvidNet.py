# -*- coding: utf-8 -*-

import re
from module.plugins.internal.misc import parse_size
from module.plugins.internal.SimpleHoster import SimpleHoster

class SpeedvidNet(SimpleHoster):
    __name__ = "SpeedvidNet"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"https?://(?:\w*\.)*(?P<DOMAIN>speedvid\.net)/(?:.*id=|.*file_code=|embed-)?(?P<id>\w{12})"
    __description__ = """speedvid.net plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    HOSTERDOMAIN = 'speedvid.net'
    INFO_PATTERN = r'<div class="dltitre">(?P<N>[^<]*)'
    LINK_PATTERN = r'"(https?://[^"]*)"[^>]*>Direct Download Link'
    CGI_INTERFACE = '/dl'
    VERSION_PATTERN = r"onclick=\"download_video\('(?P<id>\w*?)','(?P<short>.)','(?P<long>[^']*)'\)\">(?P<qual>[^<]*)</a>.*?(?P<resx>\d+)[0-9x]*,\s*(?P<size>[^<]*)<"
    DL_ORIG_PATTERN = r'name="op".*value="download_orig"'

    URL_REPLACEMENTS = [(__pattern__ + ".*", 'http://' + HOSTERDOMAIN + '/dl?op=download_orig&id=\g<id>')]

    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1
        self.resumeDownload = True


    def handle_free(self, pyfile):
        file_id = re.search(self.__pattern__, pyfile.url).group('id')
        self.data = self.load('http://' + self.HOSTERDOMAIN + self.CGI_INTERFACE + '?op=get_vid_versions&file_code=%s' % file_id)

        # get the best quality version
        available_versions = re.findall(self.VERSION_PATTERN, self.data)
        self.log_info(_("%d versions available" % len(available_versions)))
        infos = dict()
        for the_id, short_url, long_url, qual, resx, size in available_versions:
            infos[resx] = {'id': the_id, 'mode': short_url, 'hash': long_url, 'size': size}
        
        self.log_debug('versions: %s' % str(infos))

        # get best quality page
        largest_x_res = max(infos, key=int)
        self.info['size'] = parse_size(infos[largest_x_res]['size'])
        self.data = self.load(self.pyfile.url, post={'op': 'download_orig', 
                                                     'id': infos[largest_x_res]['id'],
                                                     'mode': infos[largest_x_res]['mode'],
                                                     'hash': infos[largest_x_res]['hash'],
                                                     'dl':'Download Video'})

        # sometimes, we're not getting directly to the video, but to a page with a "Download Original Video" button
        for i in range(0,4):
            if re.search(self.DL_ORIG_PATTERN, self.data) is None:
                break
            # in this case, press the button to get to the site containing the link
            action, inputs = self.parse_html_form('F1')
            self.log_debug('parsed inputs: %s' % str(inputs))
            self.data = self.load(self.pyfile.url, post=inputs)

        # get file from there
        self.link = re.search(self.LINK_PATTERN, self.data).group(1)


