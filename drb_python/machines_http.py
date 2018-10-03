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

from api_http import ApiHttp
from http_exceptions import AuthorizationError, ConnectionError
from drb_exceptions import  ActionError


class MachinesHttp(ApiHttp):
    """
     All HTTP based API Calls related to Machines
    """
    def __init__(self, host, login, verifyCert=False):
        ApiHttp.__init__(self, host, login, verifyCert)

    def get_all_machines(self):
        try:
            result = self.httpProxy.get('machines')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_machine(self, uuid):
        try:
            result = self.httpProxy.get('machines', uuid)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def create_machine(self, machine):
        try:
            result = self.httpProxy.post('machines', machine)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def update_machine(self, machine):
        try:
            result = self.httpProxy.put('machines', machine)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def delete_machine(self, uuid):
        try:
            result = self.httpProxy.delete('machines', uuid)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_all_machines_params(self):
        try:
            result = self.httpProxy.get('machines')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_machine_params(self, uuid):
        try:
            result = self.httpProxy.get('machines', uuid)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def create_machine_params(self, uuid, param):
        try:
            result = self.httpProxy.post('machines'/ + uuid + '/params', param)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def create_single_machine_param(self, uuid, key, param):
        try:
            result = self.httpProxy.post('machines'/ + uuid + '/params/' + key, param)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def delete_machine_params(self, uuid):
        try:
            result = self.httpProxy.delete('machines', uuid)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_machine_all_actions(self, uuid):
        try:
            result = self.httpProxy.get('machines/' + uuid + '/actions')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error


    def get_machine_action(self, uuid, cmd):
        try:
            result = self.httpProxy.get('machines/' + uuid + '/actions', cmd)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def execute_machine_action(self, uuid, cmd):
        try:
            result = self.httpProxy.post('machines/' + uuid + '/actions/' + cmd, {})
            if result == 400:
                raise ActionError(cmd, 'Action is not available on machine ' + uuid)
            else:
                return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_machine_pubkey(self, uuid):
        try:
            result = self.httpProxy.get('machines/' + uuid + '/pubkey')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error
