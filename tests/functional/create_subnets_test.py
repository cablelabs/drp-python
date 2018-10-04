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

from drb_python.subnets_http import SubnetsHttp
from drb_python.api_http import ConnectionStatus
from drb_python.http_exceptions import AuthorizationError, ConnectionError
from drb_python.drb_exceptions import ActionError, AlreadyExists
from subnet import Subnet
from http_session import HttpSession



class SubnetHttps(unittest.TestCase):
    """
    Tests for functions located in SubnetHttps
    """

    def test_create_subnet(self):
        login = {'username': 'rocketskates', 'password': 'r0cketsk8ts'}
        subnetObject = {
            'address': '10.197.111.0',
            'broadcast_address': '10.197.111.255',
            'default_lease': 7600,
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

        try:
            session = HttpSession('https://10.197.113.130:8092', login['username'], login['password'])

            subnet = Subnet(session, **subnetObject)
            subnet.create()

            print subnet.fetch()

            subnet.delete()

        except ConnectionError as err:
            print err
            self.fail(err)
        except AuthorizationError as err:
            print err
            self.fail(err)
        except AlreadyExists as err:
            print err
            self.fail(err)
        except ActionError as err:
            self.assertEqual(err.message, 'Action is not avalible on subnet ens5')
            self.assertEqual(err.expression, 'tests')
            result = r.delete_subnet('ens5')
            self.assertEqual(result['Name'], 'ens5')
            self.assertEqual(result['Subnet'], '10.1.1.10/24')
