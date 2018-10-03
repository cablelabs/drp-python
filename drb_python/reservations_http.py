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


class ReservationsHttp(ApiHttp):
    """
     All HTTP based API Calls related to Reservations
    """
    def __init__(self, host, login, verifyCert=False):
        ApiHttp.__init__(self, host, login, verifyCert)

    def get_all_reservations(self):
        try:
            result = self.httpProxy.get('reservations')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_reservation(self, address):
        try:
            result = self.httpProxy.get('reservations', address)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def create_reservation(self, reservation):
        try:
            result = self.httpProxy.post('reservations', reservation)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def update_reservation(self, reservation, address):
        try:
            result = self.httpProxy.put('reservations', reservation, address)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def delete_reservation(self, address):
        try:
            result = self.httpProxy.delete('reservations', address)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_reservation_all_actions(self, address):
        try:
            result = self.httpProxy.get('reservations/' + address + '/actions')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_reservation_action(self, address, cmd):
        try:
            result = self.httpProxy.get('reservations/' + address + '/actions', cmd)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def execute_reservation_action(self, address, cmd):
        try:
            result = self.httpProxy.post('reservations/' + address + '/actions/' + cmd, {})
            if result == 400:
                raise ActionError(cmd, 'Action is not available on reservation ' + address)
            else:
                return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error
