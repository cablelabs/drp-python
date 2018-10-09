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

from drp_python.model_layer.machine_config_model import MachineConfigModel

from drp_python.translation_layer.machines_translation import \
    MachineTranslation
from mock_session import MockHttpSession
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger('drp-python')


class MachineTranslationTest(unittest.TestCase):

    def setUp(self):
        self.session = MockHttpSession('http://127.0.0.1:' +
                                       '9999',
                                       'username',
                                       'password')
        self.machine_translation = MachineTranslation(self.session)

        machine_object = {
            'ip': "10.197.111.12",
            'mac': "10:7d:1a:68:0d:2f",
            'name': 'Controller',
            'os': 'ubuntu-16.04.4-server-amd64.iso',
            'type': 'management',
            'workflow': 'ubuntu16'
        }
        machine_object2 = {
            'ip': "10.197.111.12",
            'mac': "10:7d:1a:68:0d:2f",
            'name': 'Admin_Interface',
            'os': 'ubuntu-16.04.4-server-amd64.iso',
            'type': 'management',
            'workflow': 'ubuntu16'
        }
        self.machine_config_model = MachineConfigModel(**machine_object)
        self.machine_config_model2 = MachineConfigModel(**machine_object2)

    def tearDown(self):
        pass

    def test_create_machine(self):
        model = self.machine_translation.create_machine(self.machine_config_model)
        self.assertEqual(model.name, self.machine_config_model.name)
        self.assertEqual(model.ip, self.machine_config_model.ip)
        self.assertEqual(model.mac, self.machine_config_model.mac)
        self.assertEqual(model.type, self.machine_config_model.type)
        self.assertEqual(model.os, self.machine_config_model.os)
        self.assertEqual(model.workflow, self.machine_config_model.workflow)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

        model = self.machine_translation.get_machine(
            self.machine_config_model.name)
        self.assertEqual(model.name, self.machine_config_model.name)
        self.assertEqual(model.ip, self.machine_config_model.ip)
        self.assertEqual(model.mac, self.machine_config_model.mac)
        self.assertEqual(model.type, self.machine_config_model.type)
        self.assertEqual(model.os, self.machine_config_model.os)
        self.assertEqual(model.workflow, self.machine_config_model.workflow)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

    def test_update_machine(self):
        model = self.machine_translation.update_machine(
            self.machine_config_model2, self.machine_config_model.name)
        self.assertEqual(model.name, self.machine_config_model2.name)
        self.assertEqual(model.ip, self.machine_config_model2.ip)
        self.assertEqual(model.mac, self.machine_config_model2.mac)
        self.assertEqual(model.type, self.machine_config_model2.type)
        self.assertEqual(model.os, self.machine_config_model2.os)
        self.assertEqual(model.workflow, self.machine_config_model2.workflow)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

    def test_delete_machine(self):
        self.machine_translation.delete_machine(
            self.machine_config_model.name)
