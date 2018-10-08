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

from drp_python.model_layer.subnet_config_model import SubnetConfigModel

from drp_python.translation_layer.subnets_translation import \
    SubnetTranslation
from mock_session import MockHttpSession
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger('drp-python')


class HttpSessionTest(unittest.TestCase):

    def setUp(self):
        self.session = MockHttpSession('http://127.0.0.1:' +
                                       '9999',
                                       'username',
                                       'password')
        self.subnet_translation = SubnetTranslation(self.session)

        subnet_object = {
            'address': '10.197.111.0',
            'broadcast_address': '10.197.111.255',
            'default_lease': 7200,
            'dn': 'cablelabs.com',
            'dns': '8.8.8.8',
            'listen_iface': 'eno1',
            'max_lease': 7200,
            'name': 'TestSubnet',
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
            'name': 'TestSubnet',
            'netmask': '255.255.255.0',
            'range': '10.197.111.12 10.197.111.26',
            'router': '10.197.111.2',
            'type': 'management'
        }
        self.subnet_config_model = SubnetConfigModel(**subnet_object)
        self.subnet_config_model2 = SubnetConfigModel(**subnet_object2)

    def tearDown(self):
        pass

    def test_get_subnet(self):
        model = self.subnet_translation.get_subnet(
            self.subnet_config_model.name)
        self.assertEqual(model.name, self.subnet_config_model.name)
        self.assertEqual(model.address, self.subnet_config_model.address)
        self.assertEqual(model.broadcast_address,
                         self.subnet_config_model.broadcast_address)
        self.assertEqual(model.default_lease,
                         self.subnet_config_model.default_lease)
        self.assertEqual(model.dn, self.subnet_config_model.dn)
        self.assertEqual(model.dns, self.subnet_config_model.dns)
        self.assertEqual(model.listen_iface,
                         self.subnet_config_model.listen_iface)
        self.assertEqual(model.max_lease, self.subnet_config_model.max_lease)
        self.assertEqual(model.netmask, self.subnet_config_model.netmask)
        self.assertEqual(model.range, self.subnet_config_model.range)
        self.assertEqual(model.router, self.subnet_config_model.router)
        self.assertEqual(model.type, self.subnet_config_model.type)
        self.assertEquals(model.extension, {})
        self.assertEqual(model.available, True)
        self.assertEqual(model.errors, [])
        self.assertEqual(model.validated, True)
        self.assertEqual(model.options, [{u'Code': 6, u'Value': u'8.8.8.8'},
                                         {u'Code': 15,
                                          u'Value': u'cablelabs.com'},
                                         {u'Code': 1,
                                          u'Value': u'255.255.255.0'},
                                         {u'Code': 3,
                                          u'Value': u'10.197.111.1'},
                                         {u'Code': 28,
                                          u'Value': u'10.197.111.255'}])
        self.assertEqual(model.pickers, ['hint'])
        self.assertEqual(model.strategy, 'MAC')

    def test_create_subnet(self):
        model = self.subnet_translation.create_subnet(self.subnet_config_model)
        self.assertEqual(model.name, self.subnet_config_model.name)
        self.assertEqual(model.address, self.subnet_config_model.address)
        self.assertEqual(model.broadcast_address,
                         self.subnet_config_model.broadcast_address)
        self.assertEqual(model.default_lease,
                         self.subnet_config_model.default_lease)
        self.assertEqual(model.dn, self.subnet_config_model.dn)
        self.assertEqual(model.dns, self.subnet_config_model.dns)
        self.assertEqual(model.listen_iface,
                         self.subnet_config_model.listen_iface)
        self.assertEqual(model.max_lease, self.subnet_config_model.max_lease)
        self.assertEqual(model.netmask, self.subnet_config_model.netmask)
        self.assertEqual(model.range, self.subnet_config_model.range)
        self.assertEqual(model.router, self.subnet_config_model.router)
        self.assertEqual(model.type, self.subnet_config_model.type)
        self.assertEquals(model.extension, {})
        self.assertEqual(model.available, True)
        self.assertEqual(model.errors, [])
        self.assertEqual(model.validated, True)
        self.assertEqual(model.options, [{u'Code': 6, u'Value': u'8.8.8.8'},
                                         {u'Code': 15,
                                          u'Value': u'cablelabs.com'},
                                         {u'Code': 1,
                                          u'Value': u'255.255.255.0'},
                                         {u'Code': 3,
                                          u'Value': u'10.197.111.1'},
                                         {u'Code': 28,
                                          u'Value': u'10.197.111.255'}])
        self.assertEqual(model.pickers, ['hint'])
        self.assertEqual(model.strategy, 'MAC')

    def test_delete_subnet(self):
        self.subnet_translation.delete_subnet(
            self.subnet_config_model.name)

    def test_update_subnet(self):
        model = self.subnet_translation.update_subnet(
            self.subnet_config_model2, self.subnet_config_model.name)
        self.assertEqual(model.name, self.subnet_config_model2.name)
        self.assertEqual(model.address, self.subnet_config_model2.address)
        self.assertEqual(model.broadcast_address,
                         self.subnet_config_model2.broadcast_address)
        self.assertEqual(model.default_lease,
                         self.subnet_config_model2.default_lease)
        self.assertEqual(model.dn, self.subnet_config_model2.dn)
        self.assertEqual(model.dns, self.subnet_config_model2.dns)
        self.assertEqual(model.listen_iface,
                         self.subnet_config_model2.listen_iface)
        self.assertEqual(model.max_lease, self.subnet_config_model2.max_lease)
        self.assertEqual(model.netmask, self.subnet_config_model2.netmask)
        self.assertEqual(model.range, self.subnet_config_model2.range)
        self.assertEqual(model.router, self.subnet_config_model2.router)
        self.assertEqual(model.type, self.subnet_config_model2.type)
        self.assertEquals(model.extension, {})
        self.assertEqual(model.available, True)
        self.assertEqual(model.errors, [])
        self.assertEqual(model.validated, True)
        self.assertEqual(model.options, [
            {'Code': 6, 'Description': 'Domain Name Server',
             'Value': '8.8.8.8'},
            {'Code': 15, 'Description': 'Domain Name',
             'Value': 'cablelabs.com'},
            {'Code': 1, 'Description': 'Network Mask',
             'Value': '255.255.255.0'},
            {'Code': 3, 'Description': 'Router', 'Value': '10.197.111.2'},
            {'Code': 28, 'Description': 'Broadcast Address',
             'Value': '10.197.111.255'}])
        self.assertEqual(model.pickers, ['hint'])
        self.assertEqual(model.strategy, 'MAC')
