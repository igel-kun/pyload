# -*- coding: utf-8 -*-

import os
import xml.etree.cElementTree as ET

from module.plugins.internal.misc import fixurl, parse_name, safejoin, encode, exists

from module.plugins.internal.XFSHoster import XFSHoster
from module.plugins.hoster.JWPlayerBased import JWPlayerBased
from module.network.RTMPDownload import RTMPDownload

def parse_smil(smil):
    root = ET.fromstring(smil)
    rtmp_url = root.find('.//meta[@base]').attrib['base']
    streamname = root.find('.//video[@src]').attrib['src']
    return rtmp_url, streamname

class NosvideoCom(JWPlayerBased):
    __name__ = "NosvideoCom"
    __type__ = "hoster"
    __version__ = "0.01"
    __status__ = "testing"
    __pattern__ = r'(?:https?://)?(?:\w*\.)*nosvideo\.com/?(?:v=)?(?P<id>\w*)'
    __config__  = [("activated"         , "bool"          , "Activated"                                        , True     )]

    __description__ = """NosvideoCom plugin"""
    __author_name__ = ("igel")
    __author_mail__ = ("")

    BASE_URL = 'http://nosvideo.com/'
    NAME_PATTERN = XFSHoster.NAME_PATTERN
    #NAME_PATTERN = r'(?:name="fname"[ ]+value="|<[\w^_]+ class="(file)?name">)\s*(?P<N>.+?)(?:\s*<|")'

    JW_PATTERN = None
    JW_LINK_PATTERN = r"<script>var.*(http.*?smil)"

    # TODO: a SMIL file can be parsed off the webpage in plain text and then used in rtmpdump -r <url> -y <streamname> -o <output file>


    def process(self, pyfile):
        # preprocessing: preload, check for errors & duplicates and get infos
        self._prepare()
        self._preload()
        self.grab_info()
        self.check_duplicates()
        if self.info.get('status', 7) != 2:
            self.check_errors()
            self.check_status()

        # call the JWPlayerBased's handle_free to get the address of the SMIL file into self.link
        super(NosvideoCom, self).handle_free(pyfile)

        data = self.load(self.link)
        self.log_debug('parsing smil: %s' % data)

        try:
            rtmp_url, streamname = parse_smil(data)
            self.download(rtmp_url, streamname)
        except Exception, e:
            self.error(e.message)



    def download(self, rtmp_url, streamname):
        if self.pyload.debug:
            self.log_debug("DOWNLOAD RTMP " + rtmp_url + " STREAM " + streamname,
                           *["%s=%s" % (key, value) for key, value in locals().items()
                             if key not in ("self", "rtmp_url", "streamname", "_[1]")])

        dl_url      = fixurl(rtmp_url)
        dl_basename = parse_name(self.pyfile.name)
        self.pyfile.name = dl_basename

        dl_folder   = self.pyload.config.get('general', 'download_folder')
        dl_dirname  = safejoin(dl_folder, self.pyfile.package().folder)
        dl_filename = safejoin(dl_dirname, dl_basename)
        dl_dir  = encode(dl_dirname)
        dl_file = encode(dl_filename)

        if not exists(dl_dir):
            os.makedirs(dl_dir)

        self.set_permissions(dl_dir)

        self.pyfile.setStatus("downloading")
        self.pyload.hookManager.dispatchEvent("download_start", self.pyfile, dl_url, dl_filename)

        dl = RTMPDownload(rtmp_url, playpath=streamname, filename=dl_filename)
        dl.download()

        self.log_debug('done downloading RTMP stream to %s' % str(dl_filename))

        self.set_permissions(dl_file)
        self.last_download = dl_filename

        return dl_filename

