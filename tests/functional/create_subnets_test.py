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

from drb_python.http_exceptions import AuthorizationError, ConnectionError
from drb_python.drb_exceptions import ActionError, AlreadyExists
from drb_python.subnet import Subnet
from drb_python.http_session import HttpSession


class SubnetTest(unittest.TestCase):
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

        try:
            session = HttpSession('https://10.197.113.130:8092', login['username'], login['password'])

            subnet = Subnet(session, **subnet_object)
            self.assertTrue(subnet.create())
            self.assertTrue(subnet.fetch())
            temp = subnet.get()
            for key in temp:
                self.assertEqual(subnet_object[key], temp[key])
            for key in subnet_object:
                self.assertEqual(subnet_object[key], temp[key])

            temp = subnet.get_all()
            self.assertEqual(len(temp), 1)

            subnet.update(**subnet_object2)

            temp = subnet.get()
            for key in temp:
                self.assertEqual(subnet_object2[key], temp[key])
            for key in subnet_object2:
                self.assertEqual(subnet_object2[key], temp[key])

            self.assertTrue(subnet.delete())

        except ConnectionError as err:
            print err
            self.fail(err)
        except AuthorizationError as err:
            print err
            self.fail(err)
        except AlreadyExists as err:
            print err
            self.fail(err)
