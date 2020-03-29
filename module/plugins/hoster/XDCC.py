# -*- coding: utf-8 -*-

import os
import re

from module.plugins.internal.Hoster import Hoster
from module.network.XDCCRequest import XDCCRequest
from module.plugins.internal.misc import parse_name, safejoin

class XDCC(Hoster):
    __name__    = "XDCC"
    __type__    = "hoster"
    __version__ = "99"
    __status__  = "testing"

    __pattern__ = r'(?:xdcc|irc)(?P<SSL>s?)://(?P<SERVER>.*?)/#?(?P<CHAN>.*?)/(?P<BOT>.*?)/#?(?P<PACK>\d+)/?'

    # mimic IRSSI v0.8.6 by default
    __config__  = [("nick",          "str", "Nickname",           "pyload"               ),
                   ("passowrd",      "str", "Password for the nickname", ""              ),
                   ("realname",      "str", "Realname",           "really pyload"        ),
                   ("ctcp_version",  "str", "Version string to send on CTCP VERSION requests", "irssi v0.8.6 - running on FreeBSD i686"),
                   ("passive_port",  "str", "Local port to open for passive DCC - 0 for auto select, X-Y for a range",  0)]

    __description__ = """Download from IRC XDCC bot"""
    __license__     = "GPLv3"
    __authors__     = [("jeix",      "jeix@hasnomail.com"        ),
                       ("GammaC0de", "nitzo2001[AT]yahoo[DOT]com"),
                       ("igel", "")]

    # NETWORK rules are commands to send to the server on connection, depending on the server name
    NETWORK_RULES = [(r'abjects', ['JOIN #mg-chat']), (r'abandoned-irc', ['JOIN #zw-chat']), (r'scenep2p.net', ['JOIN #THE.LOUNGE'])]
    # PRIVMSG rules are rules to turn private messages from anyone whose name matches rule[0] into commands using re.sub(rule[1], rule[2])
    PRIVMSG_RULES = [(r"(?:@staff|Zombies)", r".*you must /?join .*?(#[^ ]*) .*to download.*", r"JOIN \1")]
    # ERROR patterns are patterns that, when received as a private notice, cause the download to fail
    ERROR_PATTERN = r"(invalid pack|try again)"

    def setup(self):
        # TODO: find a way to do multiDL for different servers
        self.multiDL = False

    def parse_server(self, server, ssl):
        temp = server.split(':')
        server = temp[0]
        if len(temp) == 2:
            try:
                port = int(temp[1])
            except ValueError:
                self.fail(_("Error: Erroneous port: %s." % temp[1]))
            return (server, port)
        elif len(temp) == 1:
            return (server, 6667 if not ssl else 6697)
        else:
            self.fail(_("Invalid hostname for IRC Server: %s") % server)

    def setup_base(self):
        # check for duplicates before get_info() overwrites our perfectly good pyfile.name from a previous attempt with the silly "url"
        self.check_duplicates()

    def process(self, pyfile):
        dl_basename = parse_name(pyfile.name)
        dl_folder   = self.pyload.config.get('general', 'download_folder')
        dl_dirname  = safejoin(dl_folder, pyfile.package().folder)
        dl_filename = safejoin(dl_dirname, dl_basename)

        try:
            ssl, server, chan, bot, pack = re.match(self.__pattern__, pyfile.url).groups()
            ssl           = False if not ssl else True
            nick          = self.config.get('nick')
            password      = self.config.get('password')
            realname      = self.config.get('realname')
            # split the port from the server
            server,port = self.parse_server(server, ssl)
        except Exception:
            self.fail(_("malformed XDCC URI: %s - expected xdcc://server[:port]/chan/bot/pack" % pyfile.url))

        self.req = XDCCRequest(self, pyfile)
        self.req.download(server, port, ssl, chan, bot, pack, dl_filename, True, nick, password, realname)




