# -*- coding: utf-8 -*-

import re

from module.plugins.internal.misc import eval_js_script, get_domain
from module.plugins.internal.XFSHoster import XFSHoster


class JWPlayerBased(XFSHoster):
    __name__ = "JWPlayerBased"
    __type__ = "hoster"
    __version__ = "0.01"
    __pattern__ = r"undefined"
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """JWPlayerBased plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    INFO_PATTERN = None
    NAME_PATTERN = r'<[tT]itle>(?:[wW]atch )?(?P<N>.*?)</[Tt]itle>'
    SIZE_PATTERN = None
    LINK_PATTERN = None

    # how to find the jwplayer code in the HTML
    JW_PATTERN = r"<script .*?javascript[\"'][^>]*>\s*(eval.*?)(?:</script>|$)"

    # how to extract the link from the decoded javascript call to jwplayer
    JW_LINK_PATTERN = r"play.*?{file:[\"']([^\"']*)[\"']"

    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1
        self.resumeDownload = True

    def init(self):
        self.__pattern__ = self.pyload.pluginManager.hosterPlugins[self.classname]['pattern']

        if not self.PLUGIN_DOMAIN:
            m = re.match(self.__pattern__, self.pyfile.url)
            try:
                self.PLUGIN_DOMAIN = m.group("DOMAIN").lower()
            except:
                self.PLUGIN_DOMAIN = get_domain(m.group(0))

        self.PLUGIN_NAME   = "".join(part.capitalize() for part in re.split(r'\.|\d+|-', self.PLUGIN_DOMAIN) if part != '.')

        if not self.LINK_PATTERN:
            link_patterns = filter(None, [self.JW_PATTERN, self.JW_LINK_PATTERN])
            if link_patterns:
                self.LINK_PATTERN = "(?:%s)" % ('|'.join(link_patterns))
        self.log_debug('our link pattern is: %s' % self.LINK_PATTERN)

        if not self.ERROR_PATTERN:
            error_patterns = filter(None, [self.OFFLINE_PATTERN, self.TEMP_OFFLINE_PATTERN])
            if error_patterns:
                self.ERROR_PATTERN = "(?:%s)" % ('|'.join(error_patterns))
        self.log_debug('our error pattern is: %s' % self.ERROR_PATTERN)




    def handle_free(self, pyfile):
        self.log_debug('calling XFSs handle_free to click buttons...')
        super(JWPlayerBased, self).handle_free(pyfile)
        self.log_debug('XFSs handle_free found: %s' % str(self.link))

        if 'eval' in self.link:
            self.log_debug(_("evaluating script to get call to jwplayer"))
            js_code = re.sub('eval', '', self.link)
            data = eval_js_script(js_code)
            # now, data should be a call to jwplayer in plaintext

            # step 2: extract file URL
            m = re.search(self.JW_LINK_PATTERN, data, re.MULTILINE | re.DOTALL)
            if m is not None:
                for link_match in m.groups():
                    if link_match:
                        self.link = link_match
            else:
                self.error("could not parse call to JWplayer")


