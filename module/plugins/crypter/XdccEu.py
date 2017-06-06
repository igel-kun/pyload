# -*- coding: utf-8 -*-

import re

from module.plugins.internal.misc import eval_js_script
from module.plugins.internal.SimpleCrypter import SimpleCrypter


class XdccEu(SimpleCrypter):
    __name__    = "XdccEu"
    __type__    = "crypter"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://(?:www\.)?xdcc\.eu/'
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]


    __description__ = """XDCC.eu decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", None)]

    OFFLINE_PATTERN = r'404 Page Not Found'
    IRC_LINK_PATTERN = r'data-s="(?P<server>[^"]*)".*?data-c="(?P<channel>[^"]*)".*?<td>(?P<bot>[^<]*)</td><td>(?P<id>[^<]*)</td>'

    def process(self, pyfile):
        self.decrypt(pyfile)

    def decrypt(self, pyfile):
        self._prepare()
        self._preload()
        self.check_errors()

        self.links = self.get_links()

        # add the links to the package containing ourself
        pid = pyfile.package().id
        self.log_debug('adding links: %s' % str(self.links))
        self.pyload.api.addFiles(pid, self.links)


    def get_links(self):
        irc_links = re.findall(self.IRC_LINK_PATTERN, self.data)
        self.log_debug('found ' + str(len(irc_links)) + ' links on the site')
        links = []

        for server, channel, bot, id in irc_links:
            links.append('irc://' + server + '/' + channel + '/' + bot + '/' + id)

        return links
