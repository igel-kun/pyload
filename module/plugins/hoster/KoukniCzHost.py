# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class KoukniCzHost(SimpleHoster):
    __name__    = "KoukniCzHost"
    __type__    = "hoster"
    __version__ = "0.02"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?koukni\.cz/(\d+)'

    __description__ = """Koukni.cz hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", "")]

    LINK_PATTERN = r'"(?P<resolution>\d+)p": "(?P<link>[^"]*)"'
    NAME_PATTERN = r'property="og:title" content="([^"]*)"'


    # remember: the goal is to set self.link to something to download
    def handle_free(self, pyfile):
        self.check_errors()

        available_versions = re.findall(self.LINK_PATTERN, self.data)
        ver = dict()
        for resolution, link in available_versions:
            ver[resolution] = link

        self.log_debug('found links: %s' % str(ver))

        # get highest-quality link
        self.link = ver[max(ver, key=int)]

        # set the name of the download
        name_match = re.search(self.NAME_PATTERN, self.data)
        if name_match:
            pyfile.name = name_match.group(1) + self.link[-4:]


    def setup(self):
        self.multiDL    = True


getInfo = create_getInfo(KoukniCzHost)

