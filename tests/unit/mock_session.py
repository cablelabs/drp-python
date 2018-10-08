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


urllib3.disable_warnings()
logger = logging.getLogger('drp-python')

mock_drp = {u'Available': True, u'Subnet': u'10.197.111.0/24', u'Errors': [],
            u'Name': u'TestSubnet',
            u'Pickers': [u'hint'], u'OnlyReservations': True,
            u'Strategy': u'MAC', u'ActiveLeaseTime': 7200,
            u'Documentation': u'', u'Enabled': True,
            u'Options': [{u'Code': 6, u'Value': u'8.8.8.8'},
                         {u'Code': 15, u'Value': u'cablelabs.com'},
                         {u'Code': 1, u'Value': u'255.255.255.0'},
                         {u'Code': 3, u'Value': u'10.197.111.1'},
                         {u'Code': 28, u'Value': u'10.197.111.255'}],
            u'ReservedLeaseTime': 7200, u'ReadOnly': False, u'Meta': {},
            u'ActiveEnd': u'10.197.111.16', u'Proxy': False,
            u'NextServer': u'', u'Unmanaged': True, u'Validated': True,
            u'ActiveStart': u'10.197.111.12', u'Description': u'management'}


class MockHttpSession:
    def __init__(self, url, username, password, verify_cert=False):
        self.username = username
        self.password = password
        self.url = url
        self.token = ''
        self.verify_cert = verify_cert

    def authorize(self):
        return

    def is_authorized(self):
        return True

    def get(self, resource, key=None):
        return mock_drp

    def post(self, resource, body):
        return mock_drp

    def delete(self, resource, key):
        return mock_drp

    def put(self, resource, body, key):
        mock_drp = body
        mock_drp['Available'] = True
        mock_drp['Validated'] = True
        mock_drp['Errors'] = []


        return mock_drp
