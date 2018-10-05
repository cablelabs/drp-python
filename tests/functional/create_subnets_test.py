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

import unittest

from drb_python.subnet import Subnet
from drb_python.network_layer.http_session import HttpSession
from drb_python.exceptions.drb_exceptions import NotFoundError
import logging
from uuid import uuid4

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger('drb-python')



class SubnetTest(unittest.TestCase):

    def tearDown(self):
        if self.subnet is not None:
            self.subnet.delete()

    """
    Tests for functions located in SubnetHttps
    """

    def test_create_subnet(self):
        login = {'username': 'rocketskates', 'password': 'r0cketsk8ts'}
        subnet_object = {
            'address': '10.197.111.0',
            'broadcast_address': '10.197.111.255',
            'default_lease': 7200,
            'dn': 'cablelabs.com',
            'dns': '8.8.8.8',
            'listen_iface': 'eno1',
            'max_lease': 7200,
            'name': 'subnet' + str(uuid4()),
            'netmask': '255.255.255.0',
            'range': '10.197.111.12 10.197.111.16',
            'router': '10.197.111.1',
            'type': 'management'
        }

        subnet_object2 = {
            'address': '10.197.111.0',
            'broadcast_address': '10.197.111.255',
            'default_lease': 7600,
            'dn': 'cablelabs.com',
            'dns': '8.8.8.8',
            'listen_iface': 'eno1',
            'max_lease': 7600,
            'name': subnet_object['name'],
            'netmask': '255.255.255.0',
            'range': '10.197.111.12 10.197.111.17',
            'router': '10.197.111.1',
            'type': 'management'
        }

        session = HttpSession('https://10.197.113.130:8092', login['username'],
                              login['password'])

        self.subnet = Subnet(session, **subnet_object)
        self.subnet.create()
        self.subnet.fetch()
        temp = self.subnet.get()

        self.assertEqual(subnet_object, temp)

        temp = self.subnet.get_all()
        self.assertEqual(len(temp), 1)

        self.subnet.update(**subnet_object2)

        temp = self.subnet.get()
        self.assertEqual(subnet_object2, temp)

        self.subnet.delete()

        try:
            self.subnet.fetch()
            self.fail('Resource should be deleted')
        except NotFoundError:
            self.assertTrue(True)

