# Copyright 2018 Cable Television Laboratories, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from drp_python.exceptions.http_exceptions import AuthorizationError, \
    ConnectionError
from drp_python.exceptions.drb_exceptions import NotFoundError, \
    AlreadyExistsError
from drp_python.translation_layer.reservations_translation import \
    ReservationTranslation, \
    get_all_reservations
import logging

logger = logging.getLogger('drp-python')


class Reservation:
    """
    Client Reservation Object
    """

    def __init__(self, session, client_reservation):
        logger.debug('__init__')
        self.__reservation_config = client_reservation
        self.__api = ReservationTranslation(session)
        self.__api.open()
        try:
            self.__reservation_model = self.get()
        except NotFoundError:
            self.__reservation_model = None

    def is_valid(self):
        return self.__reservation_model is not None

    def create(self):
        logger.debug('create')
        if self.__reservation_model:
            raise AlreadyExistsError(self.__reservation_model.ip,
                                     'Reservation with that name already exists')
        else:
            self.__reservation_model = self.__api.create_reservation(
                self.__reservation_config)

    def update(self, updated_object):
        if self.__reservation_model:
            self.__reservation_model = self.__api.update_reservation(
                updated_object, self.__reservation_model.ip)
        else:
            self.__reservation_model = self.__api.create_reservation(
                updated_object)

    def delete(self):
        if self.__reservation_model:
            self.__api.delete_reservation(self.__reservation_model.ip)
            self.__reservation_model = None

    def get(self):
        return self.__api.get_reservation(self.__reservation_config.ip)


def get_all(session):
    """
    Fetches all reservations form DRP
    Note this data is not cached
    :return: List of Reservations
    """
    try:
        reservation_list = get_all_reservations(session)
        return reservation_list
    except ConnectionError as error:
        logger.error(error)
        raise error
    except AuthorizationError as error:
        logger.error(error)
        raise error
