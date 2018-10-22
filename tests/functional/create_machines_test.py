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

from drp_python.machine import Machine, get_all_machines
from drp_python.network_layer.http_session import HttpSession
from drp_python.exceptions.drb_exceptions import NotFoundError, \
    AlreadyExistsError
from drp_python.model_layer.machine_config_model import MachineConfigModel
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
machine_object = {
    'ip': "10.197.111.12",
    'mac': "10:7d:1a:68:0d:2f",
    'name': 'Controller',
    'os': 'ubuntu-16.04.4-server-amd64.iso',
    'type': 'management',
    'workflow': 'discovery'
}


class MachineTest(unittest.TestCase):

    def setUp(self):
        self.session = HttpSession('https://10.197.113.126:8092',
                                   login['username'],
                                   login['password'])

        self.machine_config_model = MachineConfigModel(**machine_object)
        self.machine = Machine(self.session, self.machine_config_model)

    def tearDown(self):
        if self.machine is not None:
            self.machine.delete()

    """
    Tests for functions located in MachineHttps
    1. Create it if it doesn't exist
    2. Verify the machine_model equals the machine_config
    3. Update the machine
    4. Verify the update matches the machine_config
    5. Get all machines
    6. Validate the count
    7. Delete the machine
    8. Validate it was deleted
    """

    def test_basic_create_machine_flow(self):
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

        temp = get_all_machines(self.session)
        count = len(temp)

        self.machine.delete()
        self.assertFalse(self.machine.is_valid())

        temp = get_all_machines(self.session)
        self.assertEqual(len(temp), count - 1)

        try:
            self.machine.get()
            self.fail('Resource should be deleted')
        except NotFoundError:
            self.assertTrue(True)

    def test_create_existing_machine_flow(self):
        self.machine.create()
        self.assertTrue(self.machine.is_valid())
        try:
            self.machine.create()
            self.fail('Should throw already exists error')
        except AlreadyExistsError as error:
            print error
