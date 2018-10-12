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

from drp_python.reservation import Reservation
from drp_python.machine import Machine
from drp_python.subnet import Subnet
from drp_python.network_layer.http_session import HttpSession
from drp_python.exceptions.drb_exceptions import NotFoundError, \
    AlreadyExistsError
from drp_python.model_layer.reservation_config_model import \
    ReservationConfigModel
from drp_python.model_layer.machine_config_model import MachineConfigModel
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

machine_object = {
    'ip': "10.197.111.12",
    'mac': "10:7d:1a:68:0d:2f",
    'name': 'Controller',
    'os': 'ubuntu-16.04.4-server-amd64.iso',
    'type': 'management',
    'workflow': 'discovery'
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

        self.machine_config_model = MachineConfigModel(**machine_object)
        self.machine = Machine(self.session, self.machine_config_model)

    def tearDown(self):
        if self.reservation is not None:
            self.reservation.delete()
        if self.subnet is not None:
            self.subnet.delete()
        if self.machine is not None:
            self.machine.delete()

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
        # subnet must exist first
        if not self.subnet.is_valid():
            self.subnet.create()
        model = self.subnet.get()
        self.assertEqual(model.address, self.subnet_config.address)
        self.assertEqual(model.broadcast_address, self.subnet_config.broadcast_address)
        self.assertEqual(model.default_lease, self.subnet_config.default_lease)
        self.assertEqual(model.dn, self.subnet_config.dn)
        self.assertEqual(model.listen_iface, self.subnet_config.listen_iface)
        self.assertEqual(model.max_lease, self.subnet_config.max_lease)
        self.assertEqual(model.netmask, self.subnet_config.netmask)
        self.assertEqual(model.range, self.subnet_config.range)
        self.assertEqual(model.router, self.subnet_config.router)
        self.assertEqual(model.type, self.subnet_config.type)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertFalse(model.read_only)

        if not self.machine.is_valid():
            self.machine.create()
        model = self.machine.get()
        self.assertIsNotNone(model.uuid)
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
        self.assertFalse(model.read_only)

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
