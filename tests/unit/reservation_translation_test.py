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

from drp_python.model_layer.reservation_config_model import ReservationConfigModel

from drp_python.translation_layer.reservations_translation import \
    ReservationTranslation
from mock_session import MockHttpSession
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.WARNING)

logger = logging.getLogger('drp-python')


class ReservationTranslationTest(unittest.TestCase):

    def setUp(self):
        self.session = MockHttpSession('http://127.0.0.1:' +
                                       '9999',
                                       'username',
                                       'password')
        self.reservation_translation = ReservationTranslation(self.session)

        reservation_object = {
            'ip': "10.197.111.12",
            'mac': "10:7d:1a:68:0d:2f",
            'name': 'Admin_Interface',
            'type': 'management',
        }
        reservation_object2 = {
            'ip': "10.197.111.12",
            'mac': "10:7d:1a:68:0d:2f",
            'name': 'Admin_Interface2',
            'type': 'management',
        }
        self.reservation_config_model = ReservationConfigModel(**reservation_object)
        self.reservation_config_model2 = ReservationConfigModel(**reservation_object2)

    def tearDown(self):
        pass

    def test_create_reservation(self):
        model = self.reservation_translation.create_reservation(self.reservation_config_model)
        self.assertEqual(model.name, self.reservation_config_model.name)
        self.assertEqual(model.ip, self.reservation_config_model.ip)
        self.assertEqual(model.mac, self.reservation_config_model.mac)
        self.assertEqual(model.type, self.reservation_config_model.type)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

        model = self.reservation_translation.get_reservation(
            self.reservation_config_model.ip)
        self.assertEqual(model.name, self.reservation_config_model.name)
        self.assertEqual(model.ip, self.reservation_config_model.ip)
        self.assertEqual(model.mac, self.reservation_config_model.mac)
        self.assertEqual(model.type, self.reservation_config_model.type)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

    def test_update_reservation(self):
        model = self.reservation_translation.update_reservation(
            self.reservation_config_model2, self.reservation_config_model.ip)
        self.assertEqual(model.name, self.reservation_config_model2.name)
        self.assertEqual(model.ip, self.reservation_config_model2.ip)
        self.assertEqual(model.mac, self.reservation_config_model2.mac)
        self.assertEqual(model.type, self.reservation_config_model2.type)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertTrue(model.read_only)

    def test_delete_reservation(self):
        self.reservation_translation.delete_reservation(
            self.reservation_config_model.ip)
