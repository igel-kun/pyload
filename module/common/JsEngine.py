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

    @author: RaNaN
"""

from __future__ import with_statement

import os
import tempfile
import urllib
from imp import find_module

ENGINE = ""
ENGINES = set()
DEBUG = False


PRINT_COMMANDS = {'js':'print',
        'pyv8':'print',
        'rhino':'print',
        'node':'console.log',
        'js2py': ''}

def call_external(command, extra_env = {}):
    my_env = os.environ.copy()
    my_env.update(extra_env)
    out, err = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env).communicate()
    return out.strip()

def compute_42(command, print_cmd):
    command.append(print_cmd + '(23+19)')
    return call_external(command)



if not ENGINES or DEBUG:
    try:
        import js2py
        out = js2py.eval_js("(23+19).toString()").strip()

        #integrity check
        if out == "42":
            ENGINES.insert("js2py")
    except:
        pass

if not ENGINES or DEBUG:
    try:
        if compute_42(["js", "-e"], PRINT_COMMANDS['js']) == "42":
            ENGINES.insert("js")
    except:
        pass


if not ENGINES or DEBUG:
    try:
        find_module("PyV8")
        ENGINES.insert("pyv8")
    except:
        pass

if not ENGINES or DEBUG:
    try:
        if compute_42(["js", "-e"], PRINT_COMMANDS['node']) == "42":
            ENGINES.insert("node")
    except:
        pass

if not ENGINES or DEBUG:
    try:
        path = "" #path where to find rhino

        if os.path.exists("/usr/share/java/js.jar"):
            path = "/usr/share/java/js.jar"
        elif os.path.exists("js.jar"):
            path = "js.jar"
        elif os.path.exists(os.path.join(pypath, "js.jar")): #may raises an exception, but js.jar wasnt found anyway
            path = os.path.join(pypath, "js.jar")

        if not path:
            raise Exception

        if compute_42(["java", "-cp", path, "org.mozilla.javascript.tools.shell.Main", "-e"], PRINT_COMMANDS['rhino']) == "42":
            ENGINES.insert("rhino")
    except:
        pass

for eng in ENGINES:
    ENGINE = eng
    break


class JsEngine():
    def __init__(self):
        self.engine = ENGINE
        self.init = False

    def __nonzero__(self):
        return False if not self.engine else True

    def eval(self, script):
        if not self.init:
            if self.engine == "pyv8" or (DEBUG and ('pyv8' in ENGINES)):
                import PyV8
                global PyV8

            self.init = True

        if type(script) == unicode:
            script = script.encode("utf8")

        if not self.engine:
            raise Exception("No JS Engine")

        if not DEBUG:
            if self.engine == "pyv8":
                return self.eval_pyv8(script)
            elif self.engine == "js2py":
                return self.eval_js2py(script)
            elif self.engine == "js":
                return self.eval_js(script)
            elif self.engine == "node":
                return self.eval_node(script)
            elif self.engine == "rhino":
                return self.eval_rhino(script)
        else:
            results = []
            if 'pyv8' in ENGINES:
                res = self.eval_pyv8(script)
                print "PyV8:", res
                results.append(res)
            if 'js2py' in ENGINES:
                res = self.eval_js2py(script)
                print "js2py:", res
                results.append(res)
            if 'js' in ENGINES:
                res = self.eval_js(script)
                print "JS:", res
                results.append(res)
            if 'node' in ENGINES:
                res = self.eval_node(script)
                print "NODE:", res
                results.append(res)
            if 'rhino' in ENGINES:
                res = self.eval_rhino(script)
                print "Rhino:", res
                results.append(res)

            warning = False
            for x in results:
                for y in results:
                    if x != y:
                        warning = True

            if warning: print "### WARNING ###: Different results"

            return results[0]

    def eval_pyv8(self, script):
        with PyV8.JSLocker():
            with PyV8.JSContext() as rt:
                return rt.eval(script)

    def eval_js(self, script):
        script = "print(eval(unescape('%s')))" % urllib.quote(script)
        if len(script) <= 2000:
            script_file = None
            p = subprocess.Popen(["js", "-e", script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        else:
            fd, script_file = tempfile.mkstemp(prefix='script_file_', suffix='.js', dir="tmp")
            os.write(fd, script)
            os.close(fd)
            p = subprocess.Popen(["js", "-f", script_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        out, err = p.communicate()
        if script_file and os.path.exists(script_file):
            os.unlink(script_file)
        res = out.strip()
        return res

    def eval_js2py(self, script):
        script = "(eval(unescape('%s'))).toString()" % urllib.quote(script)
        res = js2py.eval_js(script).strip()
        return res

    def eval_node(self, script):
        script = "console.log(eval(unescape('%s')))" % urllib.quote(script)
        if len(script) <= 2000:
            script_file = None
            p = subprocess.Popen(["node", "-e", script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        else:
            fd, script_file = tempfile.mkstemp(prefix='script_file_', suffix='.js', dir="tmp")
            os.write(fd, script)
            os.close(fd)
            p = subprocess.Popen(["node",script_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        out, err = p.communicate()
        if script_file and os.path.exists(script_file):
            os.unlink(script_file)
        res = out.strip()
        return res

    def eval_rhino(self, script):
        script = "print(eval(unescape('%s')))" % urllib.quote(script)
        if len(script) <= 1800:
            script_file = None
            p = subprocess.Popen(["java", "-cp", path, "org.mozilla.javascript.tools.shell.Main", "-e", script],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        else:
            fd, script_file = tempfile.mkstemp(prefix='script_file_', suffix='.js', dir="tmp")
            os.write(fd, script)
            os.close(fd)
            p = subprocess.Popen(["java", "-cp", path, "org.mozilla.javascript.tools.shell.Main", "-f", script_file],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        out, err = p.communicate()
        if script_file and os.path.exists(script_file):
            os.unlink(script_file)
        res = out.strip()
        return res.decode("utf8").encode("ISO-8859-1")

    def error(self):
        return _("No js engine detected, please install either js2py, Spidermonkey, ossp-js, pyv8, nodejs or rhino")

if __name__ == "__main__":
    js = JsEngine()

    test = u'"ü"+"ä"'
    js.eval(test)
