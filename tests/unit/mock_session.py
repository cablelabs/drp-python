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


import urllib3
import logging
from drp_python.exceptions.drb_exceptions import NotFoundError

urllib3.disable_warnings()
logger = logging.getLogger('drp-python')


class MockHttpSession:
    def __init__(self, url, username, password, verify_cert=False):
        self.username = username
        self.password = password
        self.url = url
        self.token = ''
        self.verify_cert = verify_cert
        self.mock_drp = None

    def authorize(self):
        return

    def is_authorized(self):
        return True

    def get(self, resource, key=None):
        if self.mock_drp is None:
            raise NotFoundError(key, 'Does not exist')
        return self.mock_drp

    def post(self, resource, body):
        self.mock_drp = body
        self.mock_drp['Available'] = True
        self.mock_drp['Validated'] = True
        self.mock_drp['Errors'] = []
        self.mock_drp['ReadOnly'] = True
        return self.mock_drp

    def delete(self, resource, key):
        return self.mock_drp

    def put(self, resource, body, key):
        self.mock_drp = body
        self.mock_drp['Available'] = True
        self.mock_drp['Validated'] = True
        self.mock_drp['Errors'] = []
        self.mock_drp['ReadOnly'] = True
        return self.mock_drp
