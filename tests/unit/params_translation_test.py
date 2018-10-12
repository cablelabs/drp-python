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

from drp_python.model_layer.params_config_model import ParamsConfigModel

from drp_python.translation_layer.params_translation import \
    ParamsTranslation
from mock_session import MockHttpSession
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.WARNING)

logger = logging.getLogger('drp-python')


# "mgmt": mgmt_ip, "tenant": tenant_ip, "data":ext_ip

class ParamsTranslationTest(unittest.TestCase):

    def setUp(self):
        self.session = MockHttpSession('http://127.0.0.1:' +
                                       '9999',
                                       'username',
                                       'password')
        self.params_translation = ParamsTranslation(self.session)

        params_object = {
            'name': "mgmt",
            'value': "10.197,111.12",
            'description': 'Admin_Interface',
            'type': 'management',
            'schema': {
                'type': 'string'
            }
        }

        self.params_config_model = ParamsConfigModel(**params_object)

    def tearDown(self):
        pass

    def test_create_params(self):
        model = self.params_translation.create_params(self.params_config_model)
        self.assertEqual(model.name, self.params_config_model.name)
        self.assertEqual(model.value, None)
        self.assertEqual(model.description,
                         self.params_config_model.description)
        self.assertEqual(model.type, self.params_config_model.type)
        self.assertEqual(model.schema, self.params_config_model.schema)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

        model = self.params_translation.get_params(
            self.params_config_model.name)
        self.assertEqual(model.name, self.params_config_model.name)
        self.assertEqual(model.value, None)
        self.assertEqual(model.description,
                         self.params_config_model.description)
        self.assertEqual(model.type, self.params_config_model.type)
        self.assertEqual(model.schema, self.params_config_model.schema)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

    def test_delete_params(self):
        self.params_translation.delete_params(
            self.params_config_model.name)
