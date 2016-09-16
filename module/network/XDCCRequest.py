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
    
    @author: igel
"""

import re
import os
import struct
import shlex
import random   # to get a random nick in case our nickname is already in use
import time
import socket # for exceptions and DNS

# we're going to use jaraco's python-irc library found
# here: https://github.com/jaraco/irc
# or on debian-based linux: apt-get install python-irc
import irc.client

# we're changing state as follows 
# TODO: make sure to avoid race conditions
# processing  = connecting to server, joining channel, and contacting bot
# waiting     = waiting for bot to answer
# starting    = negotiating and preparing DCC connection
# downloading = receiving file


# TODO: resume support

from module.plugins.Plugin import Abort, Fail, SkipDownload as Skip;
from module.plugins.internal.misc import exists, encode



# use this custom exception to allow exiting the "while 1:" loop used by irc.client
class Disconnect(Exception):
    pass

class XDCCRequest(irc.client.SimpleIRCClient):
    # IP query related
    whois_target = None
    whois_answer = None
    userip_target = None
    userip_answer = None

    # some bots ignore private messages but need to be messaged by ctcp
    # this variable keeps track of whether we fell back on ctcp already
    ctcp_fellback = False

    # progress-related
    last_speeds = []
    last_speed_measure_time = 0
    last_speed_measure_bytes = 0
    speed_average_over = 5


    def __init__(self, plugin, pyfile):
        irc.client.SimpleIRCClient.__init__(self)
        self.plugin = plugin
        self.pyfile = pyfile
        self.size = 0
        self.arrived = 0


    def download(self, server, port, channel, botname, request, filename, disposition = True,
            nick = "pyload", password = None, realname = None):
        self.channel = channel
        self.botname = botname
        self.request = request
        self.filename = filename
        self.disposition = disposition

        self.plugin.log_debug('connecting to %s:%d as %s' %(server, port, nick))
        self.pyfile.setStatus("processing")
        try:
            self.connect(server, port, nick, password, nick, realname)
            # replace non-UTF8 characters, otherwise, the connection may crash on receiving non-UTF8 chars
            self.connection.buffer.errors = 'replace'
            self.start()
        except irc.client.ServerConnectionError as x:
            #NOTE: if the ServerConnection chickened out on us, we wont have to self.close(), so no reason to catch Disconnect
            # if the server refused connection, we might have behaved badly in the past
            if "Connection refused" in str(x):
                self.plugin.temp_offline(_("IRC server refused connection. Have we been naughty?"))
            else:
                self.plugin.fail(_("failed to connect to %s:%d as %s because: %s" % (server, port, nick, str(x))))
        except (Abort, Fail, Skip) as e:
            # on abort or fail, call close() which will raise Disconnect
            self.plugin.log_debug("XDCC - abort|fail|skip called, closing connections")
            try:
                self.connection.quit()
            except Disconnect:
                pass
            raise e
        except Disconnect:
            pass
        self.plugin.log_debug("XDCC subroutine exited gracefully")



    def request_via_ctcp(self, connection):
        # some bots are known to not react to private messages, but only to CTCP requests
        # so, if we're still waiting for an answer, try to send via ctcp instead
        if self.pyfile.hasStatus('waiting'):
            self.plugin.log_debug("XDCC - no answer to our request, requesting %s from %s using CTCP" % (self.request, self.botname))
            connection.ctcp("XDCC", self.botname, "SEND " + self.request)


    def request_via_privmsg(self, connection):
        connection.privmsg(self.botname, "XDCC SEND " + self.request)


    def on_join(self, connection, event):
        # it seems that irc.client calls this way too often while we're downloading
        if self.pyfile.hasStatus("processing"):
            self.pyfile.setStatus("waiting")
            self.request_via_privmsg(connection)
            # schedule to repeat the request via CTCP in 30s as some bots don't respond to PRIVMSGs
            self.ircobj.execute_delayed(30, self.request_via_ctcp, [connection])


    # try joining the given channel, prepend a '#' if neccessary
    def on_welcome(self, connection, event):
        self.external_ip = self.parse_ip_from_message(" ".join(event.arguments))
        self.plugin.log_debug("XDCC - parsed external IP %s from welcome message: %s" % (str(self.external_ip), str(event.arguments)))

        self.plugin.log_debug("XDCC - joining channel " + self.channel)
        if irc.client.is_channel(self.channel):
            connection.join(self.channel)
        else:
            self.channel = "#" + self.channel
            if irc.client.is_channel(self.channel):
                connection.join(self.channel)
            else:
                self.plugin.fail(_("no channel named ") + self.channel)


    def on_nosuchnick(self, connection, event):
        self.plugin.fail(_("noone named " + self.botname + " exists on the server"))

    def on_nicknameinuse(self, connection, event):
        current_nick = self.connection.get_nickname()
        new_nick = current_nick + str(int(random.random() * 10000))
        self.plugin.log_debug('our nick (%s) is already in use, using %s instead' % (current_nick, new_nick))
        connection.nick(new_nick)

    # active ctcp connections: SEND <FILENAME> <ADDRESS> <PORT> [SIZE]
    # passive ctcp connections: SEND <FILENAME> <ADDRESS>   0   <SIZE> <ID>
    def parse_ctcp_command(self, arguments):
        result = dict()
        result['command'] = arguments[0]
        if result['command'] in ("DCC", "XDCC"):
            parts = shlex.split(arguments[1])
            if parts[0] == "SEND":
                result.update({'filename' : parts[1], 'address' : irc.client.ip_numstr_to_quad(parts[2]), 'port': int(parts[3])})
                result['passive'] = (result['port'] == 0)
                if len(parts) >= 5:
                    result['size'] = int(parts[4])
                if result['passive']:
                    result['id'] = parts[5]
        return result


    def on_ctcp(self, connection, event):
        self.plugin.log_debug("handling CTCP command: %s" % str(event.arguments))
        try:
            command = self.parse_ctcp_command(event.arguments)
            if command['command'] == "VERSION":
                connection.ctcp("VERSION", self.botname, self.plugin.config.get("ctcp_version", "pyload"))
            elif command['command'] == "TIME":
                connection.ctcp("TIME", self.botname, time.strftime("%a $d %b %Y %H:%M:%S %z"))
            elif command['command'] == "PING":
                connection.ctcp("PING", self.botname, event.arguments[1])
            elif command['command'] in ("DCC", "XDCC"):
                self.receive_dcc(connection, command)
            elif command['command'] in ("SLOTS","MP3"):
                # ignore pesky SLOTS and MP3 announcements
                return
            else:
                self.plugin.log_debug("ignoring unknown CTCP command %s" % str(event.arguments))
                return
        except socket.timeout as e:
            self.plugin.fail("bot did not open DCC on %s:%d as promised (error: %s)" % (commands['address'], commands['port'], str(e)))
        except (Abort, Fail, Skip) as e:
            raise e
        except Exception as e:
            self.plugin.fail("error handling CTCP message %s (error: %s)" % (str(event.arguments), str(e)))


    def prepare_file(self):
        self.plugin.info.update({'name': os.path.basename(self.filename), 'size': self.size, 'status':2})
        self.plugin.sync_info()
        self.plugin.check_duplicates()

        # create the directory
        dl_dir = encode(os.path.dirname(self.filename))
        if not exists(dl_dir):
            try:
                os.makedirs(dl_dir)
            except Exception as e:
                self.plugin.fail(e.message)

        self.plugin.log_debug("XDCC - writing file to " + self.filename)
        self.plugin.set_permissions(dl_dir)
        self.file = open(self.filename, "wb")


    def receive_dcc(self, connection, command):
        self.pyfile.setStatus("starting")

        # if the connection is passive, we will need the external IP address first, so dispatch to get it
        if command['passive'] and not self.external_ip:
            self.plugin.log_debug("XDCC - detected passive DCC, getting external IP first...")
            self.get_external_address(connection)
            self.ircobj.execute_delayed(25, self.receive_dcc, [command])
            return

        self.plugin.log_debug("XDCC - translated answer: %s " % command)

        # update names if disposition is requested
        if self.disposition:
            self.filename = os.path.join(os.path.dirname(self.filename), os.path.basename(command['filename']))
            self.pyfile.name = self.filename

        # save the size for progress calculation
        self.size = command['size']

        self.prepare_file()

        self.pyfile.setStatus("downloading")
        if command['passive']:
            port = self.plugin.config.get("passive_port",0)
            internal_ip = connection.socket.getsockname()[0]
            self.plugin.log_debug("XDCC - entering passive mode, trying to use address %s:%d (external IP: %s)" % (internal_ip, port, self.external_ip))
            # note: depending on the version of python-irc, dcc_listen() takes a port or not, so try with a port first
            # in order to allow users behind firewalls or routers to have a constant port forwarded
            try:
                # the plugin can configure the port to use on passive connections
                # if no port is configured, use port 0, meaning "OS default" which, for linux, means open any free port > 1024
                self.dcc = self.dcc_listen("raw", internal_ip, port)
            except TypeError:
                self.plugin.log_debug("detected old python-irc, working around it...")
                # setup all the variables & buffers for the socket
                self.dcc = self.dcc_listen("raw")
                try:
                    # close the old socket and make a new one
                    self.dcc.socket.shutdown(socket.SHUT_RDWR)
                    self.dcc.socket.close()
                    self.dcc.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.dcc.socket.bind((internal_ip, port))
                    self.dcc.localaddress, self.dcc.localport = self.dcc.socket.getsockname()
                    self.dcc.socket.listen(10)
                except socket.error as x:
                    raise DCCConnectionError("Couldn't bind socket: %s" % x)

            self.plugin.log_debug("XDCC - listening on %s:%d for incoming DCC from %s" % (self.dcc.localaddress, self.dcc.localport, command['address']))
            connection.ctcp(command['command'], self.botname, 'SEND "%s" %s %d %d %s' % (command['filename'], irc.client.ip_quad_to_numstr(self.external_ip), self.dcc.localport, command['size'], command['id']))
            
        else:
            self.plugin.log_debug("XDCC - connecting to %s:%d" % (command['address'], command['port']))
            self.dcc = self.dcc_connect(command['address'], command['port'], "raw")
        
        self.plugin.pyload.hookManager.dispatchEvent("download_start", self.pyfile, "XDCC", self.filename)


    def on_dccmsg(self, connection, event):
        data = event.arguments[0]
        now = time.time()
        # write data to file
        self.file.write(data)

        # update statistics
        self.update_statistics(len(data), now)

        # acknowledge receit
        self.dcc.send_bytes(struct.pack("!I", self.arrived))


    def parse_ip_from_message(self, message):
        self.plugin.log_debug("parsing IP from %s" % message)
        m = re.search("((?:[\d]+\.){3}[\d]+)", message)
        if m is not None:
            return m.group(1)
        else:
            nick = self.connection.get_nickname()
            m = re.search(r"%s@([^ ]*)" % nick, message)
            if m is not None and '.' in m.group(1):
                try:
                    return socket.gethostbyname(m.group(1))
                except Exception:
                    return None
        return None


    def get_external_address(self, connection):
        if self.userip_answer:
            self.external_ip = self.userip_answer.split("@")[-1]
        else:
            if self.whois_answer:
                self.external_ip = self.parse_ip_from_message(self.whois_answer)
            else: 
                nick = self.connection.get_nickname()
                self.query_userip_info(connection, nick)
                self.query_whois_info(connection, nick)
                # call ourself again in 20s to see if results came in
                self.ircobj.execute_delayed(10, self.get_external_address, [connection])
                return

        self.plugin.log_debug("XDCC - got external IP %s" % str(self.external_ip))


    def query_userip_info(self, connection, target):
        # need the all-event handler since WHOIS answers are sent with random numerical commands
        self.ircobj.add_global_handler("all_events", self.on_userip_answer, 0)
        self.userip_target = target
        self.userip_answer = None
        connection.send_raw("USERIP " + target)


    def on_userip_answer(self, connection, event):
        if len(event.arguments) == 1:
            if self.userip_target+"=" in event.arguments[0]:
                self.userip_answer = event.arguments[0].strip()
                self.ircobj.remove_global_handler("all_events", self.on_userip_answer)


    def query_whois_info(self, connection, target):
        # need the all-event handler since WHOIS answers are sent with random numerical commands
        self.ircobj.add_global_handler("all_events", self.on_whois_answer, 0)
        self.whois_target = target
        self.whois_answer = None
        connection.whois(target)


    def on_whois_answer(self, connection, event):
        if len(event.arguments) > 1:
            if event.arguments[0] == self.whois_target:
                self.whois_answer += " " + " ".join(event.arguments[1:])


    def on_end_of_whois(self, connection, event):
        self.ircobj.remove_global_handler("all_events", self.on_whois_answer)



    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        self.plugin.last_download = self.filename
        self.plugin.log_debug("Received file %s (%d kbytes)." % (self.filename, int(self.arrived/1024)))
        if self.pyfile.hasStatus("downloading"):
            if self.size and (self.size > self.arrived):
                self.pyfile.setStatus("failed")
            else:
                self.pyfile.setStatus("finished")
        self.connection.quit()


    def on_disconnect(self, connection, event):
        self.connection.close()
        raise Disconnect


    def update_statistics(self, amount, now):
        self.arrived += amount
        # only calc speeds once per second
        if now > self.last_speed_measure_time + 1:
            if len(self.last_speeds) > self.speed_average_over:
                del self.last_speeds[0]
            self.last_speeds.append((self.arrived - self.last_speed_measure_bytes) / (now - self.last_speed_measure_time));
            self.last_speed_measure_bytes = self.arrived
            self.last_speed_measure_time = now
        if self.size:
            self.pyfile.setProgress(int((100.0 * self.arrived) / self.size))



    @property
    def speed(self):
        return sum(self.last_speeds) / float(len(self.last_speeds))

    @property
    def percent(self):
        if not self.size: return 0
        return (self.arrived * 100) / self.size


    def abortDownloads(self):
        self.plugin.abort()


    def close(self):
        self.dcc.disconnect()

