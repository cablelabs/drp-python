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

from exceptions.http_exceptions import AuthorizationError, ConnectionError
from translation_layer.reservations_http import ReservationsHttp
from base import Base


class Reservation(Base):
    """
     Client Reservation class for interacting with DRP
    """

    def __init__(self, **config):
        super(Reservation, self).__init__(config)

    def create(self, **object):
        self.api = ReservationsHttp(self.host, self.login)
        self.api.open()
        self.object = self.api.create_reservation(object)
        return self.object

    def get_all(self):
        """
        Fetches all reservations form DRP
        Note this data is not cached
        :return: Array of Reservations
        """
        try:
            reservation_list = self.api.get_all_reservations()
            return reservation_list
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def fetch(self):
        try:
            self.object = self.api.get_reservation(self.object.name)
            return self.object
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def updated(self, **updated_object):
        try:
            self.object = self.api.update_reservation(updated_object, self.object.name)
            return self.object
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def delete(self):
        try:
            self.object = self.api.delete_reservation(self.object.name)
            return self.object
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error
