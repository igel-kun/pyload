#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.
    
    @author: RaNaN, igel
"""

#NOTE: librtmp-python does not work for us because:
#     import librtmp
#  File "/usr/local/lib/python2.7/dist-packages/librtmp/__init__.py", line 16, in <module>
#    from .logging import *
#  File "/usr/local/lib/python2.7/dist-packages/librtmp/logging.py", line 67, in <module>
#    add_signal_handler()
#  File "/usr/local/lib/python2.7/dist-packages/librtmp/utils.py", line 21, in add_signal_handler
#    signal.signal(signal.SIGINT, handler)
#ValueError: signal only works in main thread
#
# so for now, we're going to use rtmpdump...

# import librtmp


from os import fsync
from time import sleep


class RTMPChunk():
    def __init__(self, url, playpath, filename, parent):
        self.p = parent # RTMPDownload instance
        self.log = parent.log
        self.arrived = 0
        self.sleep = 0.000
        self.lastSize = 0
        self.done = False
        self.fails = 0

        self.fp = open(filename, "ab")

        #initialize RTMP session
        # librtmp seems to handle "live" streams with more care, so it produces less interruptions
        self.conn = librtmp.RTMP(url, playpath, live=True)
        # Attempt to connect
        self.conn.connect()
        # Get a file-like object to access to the stream
        self.stream = self.conn.create_stream()


    def __repr__(self):
        return "<HTTPChunk id=%d, size=%d, arrived=%d>" % (0, -1, self.arrived)

    def perform(self):
        try:
            buf = self.stream.read(2**16)
            size = len(buf)

            if size == 0:
                self.log.debug('stream download successfull: %d bytes' % int(self.arrived))
                self.done()
                return

            self.fp.write(buf)            
            self.arrived += size            

            # stream.read() seems to be blocking, so no sleep necessary unless we're over the bandwidth
            if self.p.bucket:
                sleep(self.p.bucket.consumed(size))
        except IOError:
            self.fails += 1
            self.log.debug('failed (%d/5) getting stream data' % int(self.fails))
            if self.fails >= 5:
                raise Fail('error downloading stream')

    def done(self):
        """ mark the download done and close everything """
        self.done = True
        self.close()

    def flushFile(self):
        """  flush and close file """
        self.fp.flush()
        fsync(self.fp.fileno()) #make sure everything was written to disk

    def close(self):
        """ closes everything, unusable after this """
        if self.fp: self.fp.close()
        self.stream.close()
        if hasattr(self, "p"): del self.p

