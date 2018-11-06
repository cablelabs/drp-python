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

from drp_python.reservation import Reservation, get_all_reservations
from drp_python.subnet import Subnet
from drp_python.network_layer.http_session import HttpSession
from drp_python.exceptions.drb_exceptions import NotFoundError, \
    AlreadyExistsError
from drp_python.model_layer.reservation_config_model import \
    ReservationConfigModel
from drp_python.model_layer.subnet_config_model import SubnetConfigModel
import logging
from uuid import uuid4

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.WARNING)

logger = logging.getLogger('drp-python')

# TODO: Replace this with some kinda of inject for address and such
login = {'username': 'rocketskates', 'password': 'r0cketsk8ts'}
reservation_object = {
    'ip': "10.197.111.12",
    'mac': "10:7d:1a:68:0d:2f",
    'name': 'Admin_Interface',
    'type': 'management',
}

subnet_object = {
    'address': '10.197.111.0',
    'broadcast_address': '10.197.111.255',
    'default_lease': 7200,
    'dn': 'cablelabs.com',
    'dns': '8.8.8.8',
    'listen_iface': 'eno1',
    'max_lease': 7200,
    'name': 'subnet-' + str(uuid4()),
    'netmask': '255.255.255.0',
    'range': '10.197.111.12 10.197.111.16',
    'router': '10.197.111.1',
    'next_server': '10.197.111.131',
    'type': 'management'
}


class ReservationTest(unittest.TestCase):

    def setUp(self):
        self.session = HttpSession('https://10.197.113.126:8092',
                                   login['username'],
                                   login['password'])

        self.reservation_config_model = ReservationConfigModel(
            **reservation_object)
        self.reservation = Reservation(self.session,
                                       self.reservation_config_model)

        self.subnet_config = SubnetConfigModel(**subnet_object)
        self.subnet = Subnet(self.session, self.subnet_config)
        if not self.subnet.is_valid():
            self.subnet.create()
        temp = self.subnet.get()
        self.assertEqual(self.subnet_config.address, temp.address)

    def tearDown(self):
        if self.reservation is not None:
            self.reservation.delete()
        if self.subnet is not None:
            self.subnet.delete()

    """
    Tests for functions located in ReservationHttps
    1. Create it if it doesn't exist
    2. Verify the reservation_model equals the reservation_config
    3. Update the reservation
    4. Verify the update matches the reservation_config
    5. Get all reservations
    6. Validate the count
    7. Delete the reservation
    8. Validate it was deleted
    """

    def test_basic_create_reservation_flow(self):
        if not self.reservation.is_valid():
            self.reservation.create()
        model = self.reservation.get()
        self.assertEqual(model.name, self.reservation_config_model.name)
        self.assertEqual(model.ip, self.reservation_config_model.ip)
        self.assertEqual(model.mac, self.reservation_config_model.mac)
        self.assertEqual(model.type, self.reservation_config_model.type)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertFalse(model.read_only)

        temp = get_all_reservations(self.session)
        count = len(temp)

        self.reservation.delete()
        self.assertFalse(self.reservation.is_valid())

        temp = get_all_reservations(self.session)
        self.assertEqual(len(temp), count - 1)

        try:
            self.reservation.get()
            self.fail('Resource should be deleted')
        except NotFoundError:
            self.assertTrue(True)

    def test_create_existing_reservation_flow(self):
        self.reservation.create()
        self.assertTrue(self.reservation.is_valid())
        try:
            self.reservation.create()
            self.fail('Should throw already exists error')
        except AlreadyExistsError as error:
            print error
