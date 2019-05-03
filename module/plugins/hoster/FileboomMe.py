# -*- coding: utf-8 -*-

from ..hoster.Keep2ShareCc import Keep2ShareCc


class FileboomMe(Keep2ShareCc):
    __name__ = "FileboomMe"
    __type__ = "hoster"
    __version__ = "0.10"
    __status__ = "testing"

    __pattern__ = r'https?://f(?:ile)?boom\.me/file/(?P<ID>\w+)'
    __description__ = """Fileboom.me hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("GammaC0de", None), ("igel", None)]

    URL_REPLACEMENTS = []
    API_URL = 'https://www.fileboom.me/api/v2/'

    def setup(self):
        self.resume_download = True
        self.multiDL = False
        self.chunk_limit = 1

