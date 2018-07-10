# -*- coding: utf-8 -*-


from module.plugins.internal.SimpleHoster import SimpleHoster
from module.plugins.internal.misc import seconds_to_midnight

class ShareDirCom(SimpleHoster):
    __name__    = "ShareDirCom"
    __type__    = "hoster"
    __version__ = "0.01"
    __status__  = "testing"

    __pattern__ = r'https?://dl\.sharedir\.com'
    __config__  = [("activated"   , "bool", "Activated"                                        , True)]

    __description__ = """ShareDir hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("igel", None)]

#    NAME_PATTERN = r''
#    SIZE_PATTERN = r''

    ERROR_PATTERN      = r'File not found|Sorry, this file is no longer available'
    PREMIUM_ONLY_PATTERN = r'<div class="error".*?only .*Premium users'

    def process(self, pyfile):
        self._prepare()
        
        header = self.load(pyfile.url, just_header=True)
        self.log_debug("got header: " + str(header))
        if header['content-type'] == 'text/html':
            self.data = self.load(pyfile.url)
            self.check_errors()
            # if we've got some html page, but it didn't contain an error message, then something weird happened
            self.fail('got an HTML response but no error: ' + str(self.data))
        else:
            size = int(header['content-length'])

        # first, check whether we have a chance of completing the download
        if size > self.account.get_data('maxtraffic'):
            self.fail(_("File can be downloaded by premium users only"))
        if size > self.account.get_data('trafficleft') * 1024:
            self.log_debug("we've got offered a file of size " + str(size/1024) + " KB but we've only got " + str(self.account.get_data('trafficleft')) + " KB left. So we'll dl that tomorrow")
            self.retry(wait = seconds_to_midnight())

        if self.isresource(pyfile.url):
            self.log_info(_("Downloading file from link " + str(pyfile.url) + "..."))
            self.download(pyfile.url, disposition=True)

        else:
            # if ShareDir didn't answer with a file, but with a website, parse it for errors
            self._preload()
            self.grab_info()
            self.check_status()
            # if no errors could be parse, give up
            self.fail(_("Something went wrong loading ") + pyfile.url)


