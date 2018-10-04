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

from http_exceptions import AuthorizationError, ConnectionError
from drb_exceptions import  ActionError
from machines_http import MachinesHttp
from uuid import uuid1


class Machine():
    """
     Client Machine class for interacting with DRP
    """
    def __init__(self, machine, uuid=None):
        try:
            self.machine = machine
            self.host = 'https://10.197.113.130:8092'
            self.login = {'username': 'rocketskates', 'password': 'r0cketsk8ts'}
            self.uuid = uuid
            if uuid == None:
                self.uuid = uuid1()
            self.machine['uuid'] = self.uuid
            self.machineApi = MachinesHttp(self.host, self.login)
            self.machineApi.open()
            self.machine = self.machineApi.create_machine(self.machine)
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def get_all(self):
        """
        Fetches all machines form DRP
        Note this data is not cached
        :return: Array of Machines
        """
        try:
            machine_list = self.machineApi.get_all_machines()
            return machine_list
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def get(self):
        return self.machine

    def fetch(self):
        try:
            self.machine = self.machineApi.get_machine(self.uuid)
            return self.machine
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def updated(self, updated_machine):
        try:
            self.machine = self.machineApi.update_machine(updated_machine, self.uuid)
            return self.machine
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def delete(self):
        try:
            self.machine = self.machineApi.delete_machine(self.uuid)
            return self.machine
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error
