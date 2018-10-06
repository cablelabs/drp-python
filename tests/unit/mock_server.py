# Copyright 2018 Cable Television Laboratories, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard library imports...
from BaseHTTPServer import BaseHTTPRequestHandler
import socket
import json

# Third-party imports...
import requests


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Process GET request, return a response with an HTTP 200
        # status.
        if self.headers.get('Authorization') is not None:
            data = {'Token': '123'}
            data = json.dumps(data).encode('utf-8')
            self.send_response(requests.codes.ok)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data)
            return True
        else:
            self.send_response(requests.codes.ok)
            self.end_headers()
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.send_response(requests.codes.created)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(post_body)
        return True

    def do_PUT(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(post_body)
        return True


    def do_DELETE(self):
        data = {'Deleted': '123'}
        data = json.dumps(data).encode('utf-8')
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(data)
        return True


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port
