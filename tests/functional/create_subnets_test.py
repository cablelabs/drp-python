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
from drb_python.http_session import HttpSession
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger('drb-python')

subnet = None


class SubnetTest(unittest.TestCase):

    def tearDown(self):
        if subnet is not None:
            subnet.delete()

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
            'name': 'Management_SUBNET',
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
            'name': 'Management_SUBNET',
            'netmask': '255.255.255.0',
            'range': '10.197.111.12 10.197.111.17',
            'router': '10.197.111.1',
            'type': 'management'
        }

        session = HttpSession('https://10.197.113.130:8092', login['username'],
                              login['password'])

        subnet = Subnet(session, **subnet_object)
        subnet.create()
        subnet.fetch()
        temp = subnet.get()

        self.assertEqual(subnet_object, temp)

        temp = subnet.get_all()
        self.assertEqual(len(temp), 1)

        subnet.update(**subnet_object2)

        temp = subnet.get()
        self.assertEqual(subnet_object2, temp)

        subnet.delete()
