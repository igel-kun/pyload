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

from os import remove, fsync
from os.path import dirname
from time import sleep, time
from shutil import move
from logging import getLogger
import subprocess

#from .RTMPChunk import RTMPChunk
from ..plugins.Plugin import Abort, Fail

class RTMPDownload():
    """ loads an rtmp stream """

    def __init__(self, url, playpath, filename, realtime=True, bucket=None, options=None):
        self.url = url
        self.playpath = playpath
        self.filename = filename  #complete file destination, not only name
        self.bucket = bucket
        self.proxy = {}
        if options:
            if 'proxies' in options:
                self.proxy = options['proxies']
        # all arguments

        # initialize logger
        self.log = getLogger("log")
        self.abort = False
        self.done = False

        #needed for speed calculation
        self.lastArrived = 0
        self.current_speed = 0
        self.lastSpeeds = [0, 0]

        self.command = ['rtmpdump', '-r', url, '-o', filename]
        # it appears that downloading with --realtime is much more stable, but slightly slower
        if playpath: self.command.extend(['--playpath', self.playpath])
        if realtime: self.command.append('--realtime')
        if self.proxy:
            if 'socks' in self.proxy['type']:
                self.command.extend(['--socks', str(self.proxy['address'])+':'+str(self.proxy['port'])])
#        try:
#            self.chunk = RTMPChunk(url, playpath, filename, self)
#        except:
#            raise Fail('Failed to connect')



    @property
    def speed(self):
        # return average speed over 3 measurements: speed, lastSpeed[0] and lastSpeed[1]
        last = [sum(x) for x in self.lastSpeeds if x]
        return (self.current_speed + sum(last)) / (1 + len(last))

    def download(self, resume=False):
        command = self.command
        if resume:
            command.extend(['--resume', '--skip', '1'])
        else:
            command.append('--live')
        self.log.debug('calling RTMPDUMP: %s' % str(command))
        subprocess.check_call(command)


#    def download(self):
#        lastTimeCheck = 0
#
#        while not self.chunk.done:
#            # read the stream here
#            self.chunk.perform()
#
#            # calc speed once per second, averaging over 3 seconds
#            t = time()
#            if lastTimeCheck + 1 < t:
#                diff = self.chunk.arrived - self.lastArrived
#
#                self.lastSpeeds[1] = self.lastSpeeds[0]
#                self.lastSpeeds[0] = self.current_speed
#                self.current_speed = float(diff) / (t - lastTimeCheck)
#
#                #print 'current speed: ' + str(float(self.current_speed)/1024) + ' kb/s = ' + str(diff) + 'b in ' + str(t - lastTimeCheck) + 's (sleep is ' + str(self.chunk.sleep) + 's)'
#
#                self.lastArrived = self.chunk.arrived
#                lastTimeCheck = t
#
#            if self.abort:
#                raise Abort()
#
#            #sleep(0.003) #supress busy waiting - limits dl speed to  (1 / x) * buffersize
#
#        self.chunk.flushFile() #make sure downloads are written to disk
#        self.chunk.close()
#        self.done = True


if __name__ == "__main__":
    url = 'rtmp://184.72.239.149/vod'
    playpath = 'BigBuckBunny_115k.mov'

    from Bucket import Bucket

    bucket = Bucket()
    bucket.setRate(200 * 1024)
    bucket = None

    print "starting " + url + '/' + playpath

    dwnld = RTMPDownload(url, playpath, '/tmp/Wild.flv', bucket=bucket)
    dwnld.download()

