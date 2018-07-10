# -*- coding: utf-8 -*-

import re
from module.plugins.internal.SimpleHoster import SimpleHoster


class SharesixCom(SimpleHoster):
    __name__    = "SharesixCom"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?sharesix\.com/.*'
    __description__ = """Sharesix.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]

    BASE_URL="http://www.sharesix.com"




    STAGE2_PATTERN = 'id="go-next".*?href="(.*?)">Free</a>'
    NAME_PATTERN = r'Filename:(?:.|\n)*?<dd>(.*?)</dd>'
    # the sizes seem to be inaccurate
    #SIZE_PATTERN = r'Size:(?:.|\n)*?<dd>(.*?)</dd>'
    LINK_PATTERN = r"var lnk1 = '(.*?)';"

    def handle_free(self, pyfile):
        # stage 1: Click the "Free" button
        self.html = self.load(pyfile.url)
        m = re.search(STAGE2_PATTERN, self.html)
        stage2_lnk = m.group(1)

        # stage 2: update the file information
        self.html = self.load('%s%s' % (self.BASE_URL, stage2_lnk))
        self.check_status()
        
        # stage 3: get the video link from the player
        m = re.search(LINK_PATTERN, self.html)
        link = m.group(1)

        self.download(link)



