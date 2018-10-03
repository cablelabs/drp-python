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
from drb_python.drb_exceptions import  ActionError

# subnet:
#       -
#         address: "10.197.111.0"
#         bind_host:
#           -
#             ip: "10.197.111.12"
#             mac: "10:7d:1a:68:0d:2f"
#           -
#             ip: "10.197.111.13"
#             mac: "10:7d:1a:68:0c:a9"
#           -
#             ip: "10.197.111.14"
#             mac: "10:7d:1a:68:12:e7"
#           -
#             ip: "10.197.111.15"
#             mac: "10:7d:1a:68:0c:5b"
#           -
#             ip: "10.197.111.16"
#             mac: "10:7d:1a:68:0e:9d"
#
#         broadcast-address: "10.197.111.255"
#         default-lease: 7600
#         dn: cablelabs.com
#         dns: "8.8.8.8"
#         listen_iface: eno1
#         max-lease: 7200
#         name: Managment_SUBNET
#         netmask: "255.255.255.0"
#         range: "10.197.111.12 10.197.111.16"
#         router: "10.197.111.1"
#         type: management

class SubnetHttps(unittest.TestCase):
    """
    Tests for functions located in SubnetHttps
    """
    def test_subnet(self):
        login = {'username': 'rocketskates', 'password': 'r0cketsk8ts'}
        body = {
                    u'Available': True,
                    u'Subnet': u'10.1.1.10/24',
                    u'Errors': [],
                    u'Name': u'ens5',
                    u'Pickers': [u'hint', u'nextFree', u'mostExpired'],
                    u'OnlyReservations': False,
                    u'Strategy': u'MAC',
                    u'ActiveLeaseTime': 60,
                    u'Documentation': u'',
                    u'Enabled': True,
                    u'Options': [
                        {u'Code': 3, u'Value': u'10.1.1.10'},
                        {u'Code': 6, u'Value': u'10.1.1.10'},
                        {u'Code': 15, u'Value': u'openstacklocal'},
                        {u'Code': 1, u'Value': u'255.255.255.0'},
                        {u'Code': 28, u'Value': u'10.1.1.255'}
                    ],
                    u'ReservedLeaseTime': 7200,
                    u'ReadOnly': False,
                    u'Meta': {},
                    u'ActiveEnd': u'10.1.1.254',
                    u'Proxy': False,
                    u'NextServer': u'',
                    u'Unmanaged': False,
                    u'Validated': True,
                    u'ActiveStart': u'10.1.1.10',
                    u'Description': u''
                }

        try:
            r = SubnetsHttp('https://10.197.113.130:8092', login)
            self.assertEqual(r.connectionStatus(), ConnectionStatus.CLOSED)

            r.open()
            self.assertEqual(r.connectionStatus(), ConnectionStatus.OPEN)

            result = r.delete_subnet('ens5')

            result = r.create_subnet(body)
            self.assertNotEqual(401, result)
            self.assertEqual(result['Name'], 'ens5')
            self.assertEqual(result['Subnet'], '10.1.1.10/24')

            result = r.get_all_subnets()
            self.assertNotEqual(401, result)
            self.assertEqual(1, len(result))

            result = r.get_subnet('ens5')
            self.assertEqual(result['Name'], 'ens5')
            self.assertEqual(result['Subnet'], '10.1.1.10/24')

            result = r.get_subnet_all_actions('ens5')
            self.assertEqual(result, [])

            result = r.execute_subnet_action('ens5', 'tests')
            print result
            self.assertEqual(result['Messages'], 'Action tests on subnets: Not Found')

            self.fail('Should throw ActionError on Execute test')

        except ConnectionError as err:
            print err
            self.fail(err)
        except AuthorizationError as err:
            print err
            self.fail(err)
        except ActionError as err:
            self.assertEqual(err.message, 'Action is not avalible on subnet ens5')
            self.assertEqual(err.expression, 'tests')
            result = r.delete_subnet('ens5')
            self.assertEqual(result['Name'], 'ens5')
            self.assertEqual(result['Subnet'], '10.1.1.10/24')

