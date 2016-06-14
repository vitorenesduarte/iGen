import sys
import os
from SimpleHTTPServer import SimpleHTTPRequestHandler
from i_gen import run_vc_gen
import BaseHTTPServer
import re
import simplejson
import json

class Reply:
    def __init__(self, vc, sat_or_unsat, model_or_unsat_core):
        self.vc = vc
        self.sat_or_unsat = sat_or_unsat
        self.model_or_unsat_core = model_or_unsat_core

class Replies:
    def __init__(self, vcs):
        self.vcs = vcs

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        if None != re.search('/api/v1/igen', self.path):
            if self.headers['Content-Type'] == 'application/json':
                json_string = self.rfile.read(int(self.headers['Content-Length']))
                json_decoded = simplejson.loads(json_string)
                code = json_decoded['code']
                theory = json_decoded['theory']

                result = run_vc_gen(code, theory)
                vcs = []

                for i in xrange(len(result)):
                    (vc, sat_or_unsat, model_or_unsat_core) = result[i]
                    reply = Reply(vc, sat_or_unsat, model_or_unsat_core)
                    json_reply = json.dumps(reply.__dict__)
                    vcs.append(json_reply)

                replies = Replies(vcs)
                json_replies = json.dumps(replies.__dict__)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json_replies)
            else:
                self.send_response(200)
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

if __name__ == '__main__':
    directory = "."
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        sys.argv = []
    os.chdir(directory)
    BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)
