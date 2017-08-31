# -*- coding: utf-8 -*-

############################################################################
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Affero General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Affero General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
############################################################################

import re

from module.lib.bottle import json_loads
from module.plugins.internal.SimpleCrypter import SimpleCrypter


class FilesmonsterComC(SimpleCrypter):
    __name__ = "FilesmonsterComC"
    __type__ = "crypter"
    __pattern__ = r"https?://(?:w{3}\.)?filesmonster\.com/(?:download|folders)\.php\?f?id=.*"
    __version__ = "0.02"
    __description__ = """Filesmonster.com Crypter Plugin"""
    __author_name__ = ("igel")

    LIST_PATTERN = r'<table class="table files">(.*?)</table>'
    LINK_FREE_PATTERN = r'<a href="(.*?)">'
    TEMP_OFFLINE_PATTERN = r"You have started to download"
    WAIT_PATTERN = r"will be available for download in (\d+)"
    NAME_PATTERN = r'Folder title.*?<td>(?P<N>.*?)</td>'
    SEARCH_FLAGS = {'NAME_PATTERN': re.MULTILINE | re.DOTALL}

    def get_links(self):
        # find the link to the linklist
        m = re.search(self.LIST_PATTERN, self.data, flags = re.MULTILINE | re.DOTALL)
        if m:
            self.data = m.group(1)
            return super(FilesmonsterComC, self).get_links()
        else:
            self.error(_('could not find link list'))

