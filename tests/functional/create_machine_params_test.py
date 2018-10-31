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

from drp_python.machine import Machine
from drp_python.params import Params
from drp_python.network_layer.http_session import HttpSession
from drp_python.exceptions.drb_exceptions import NotFoundError, \
    AlreadyExistsError
from drp_python.model_layer.machine_config_model import MachineConfigModel
from drp_python.model_layer.params_config_model import ParamsConfigModel
import logging

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

server_param = {
    'name': "mgmt",
    'value': "10.197.111.12",
    'description': 'Admin_Interface',
    'type': 'management',
    'schema': {
        'type': 'string'
    }
}

access_key_param = {
    "name": "access-keys",
    "value": {
        "root": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6NvYFzSKZr7RIMBYpgMbioVNS1mhM+yjIyZh9+a"
                "/Czo82Kx8HOpYN19zcV67hU6aNDfwFK701f+SIfuKznl/7nzdM1c9SMsKNrWbyGAqFGBj3gHcetI7oCqHLAL+UF6ayT8WkjdX"
                "/hYLO+hmQNdYYuu5xkdX7SzNw6eYUF9GdbL99aJ"
                "+6HLppYtA2MrmRUGevx88rkxKFnY6VaWViCqTVvKXRmgQ20ArYlMC7yUiOiOYzeoh0TMxesUjZ"
                "/RV25xXOt6RGAdK7LwrN00KQZcO9L82Rqu9WAEAmuJywD6RMLeIyJYLu9/twQQ+b5MNRg/JdEmmAmfsPtJ6cYs0zaU8z "
                "ansible-generated on ci-build-server",
        "ubuntu": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6NvYFzSKZr7RIMBYpgMbioVNS1mhM+yjIyZh9+a"
                  "/Czo82Kx8HOpYN19zcV67hU6aNDfwFK701f+SIfuKznl/7nzdM1c9SMsKNrWbyGAqFGBj3gHcetI7oCqHLAL+UF6ayT8WkjdX"
                  "/hYLO+hmQNdYYuu5xkdX7SzNw6eYUF9GdbL99aJ"
                  "+6HLppYtA2MrmRUGevx88rkxKFnY6VaWViCqTVvKXRmgQ20ArYlMC7yUiOiOYzeoh0TMxesUjZ"
                  "/RV25xXOt6RGAdK7LwrN00KQZcO9L82Rqu9WAEAmuJywD6RMLeIyJYLu9/twQQ+b5MNRg/JdEmmAmfsPtJ6cYs0zaU8z "
                  "ansible-generated on ci-build-server "
    }
}


class MachineParamTest(unittest.TestCase):

    def setUp(self):
        self.session = HttpSession('https://10.197.113.126:8092',
                                   login['username'],
                                   login['password'])

        self.machine_config_model = MachineConfigModel(**machine_object)
        self.machine = Machine(self.session, self.machine_config_model)
        self.sr_params_config_model = ParamsConfigModel(**server_param)
        self.sr_params = Params(self.session, self.sr_params_config_model)
        self.ak_params_config_model = ParamsConfigModel(**access_key_param)
        self.ak_params = Params(self.session, self.ak_params_config_model)

    def tearDown(self):
        if self.machine is not None:
            self.machine.delete()
        if self.sr_params is not None:
            self.sr_params.delete()
        # don't delete system params

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

        if not self.sr_params.is_valid():
            self.sr_params.create()
        model = self.sr_params.get()
        self.assertEqual(model.name, self.sr_params_config_model.name)
        self.assertEqual(model.value, None)
        self.assertEqual(model.description,
                         self.sr_params_config_model.description)
        self.assertEqual(model.type, self.sr_params_config_model.type)
        self.assertEqual(model.schema, self.sr_params_config_model.schema)
        self.assertEquals(model.extension, {})
        self.assertTrue(model.available)
        self.assertEqual(model.errors, [])
        self.assertTrue(model.validated)
        self.assertFalse(model.read_only)
        self.sr_params.set_machine_param(self.machine)

        model = self.machine.get()
        self.assertEqual(model.params.get(self.sr_params_config_model.name),
                         self.sr_params_config_model.value)

        if not self.ak_params.is_valid():
            self.ak_params.create()
        model = self.ak_params.get()
        self.assertEqual(model.name, self.ak_params_config_model.name)
        self.ak_params.set_machine_param(self.machine)

        model = self.machine.get()
        self.assertEqual(model.params.get(self.ak_params_config_model.name),
                         self.ak_params_config_model.value)

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
