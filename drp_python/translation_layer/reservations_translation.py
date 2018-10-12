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
from drp_python.exceptions.http_exceptions import AuthorizationError, \
    ConnectionError
from drp_python.exceptions.drb_exceptions import NotFoundError
from drp_python.model_layer.reservation_model import ReservationModel
import logging

logger = logging.getLogger('drp-python')


class ReservationTranslation(ApiHttp):
    """
     All HTTP based API Calls related to Reservations
    """

    def __init__(self, session):
        super(ReservationTranslation, self).__init__(session)
        logger.warning('__init__')

    def get_reservation(self, reservation_ip):
        logger.warning('get_reservation')
        drp_obj = self.session.get('reservations', reservation_ip)
        reservation_model = convert_to_client(drp_obj)
        return reservation_model

    def create_reservation(self, reservation_config_model):
        logger.warning('create_reservation')
        drp_object = convert_to_drp(reservation_config_model)
        drp_object = self.session.post('reservations', drp_object)
        reservation_model = convert_to_client(drp_object)
        logger.warning('Created ' + reservation_model.ip)
        return reservation_model

    def update_reservation(self, reservation_config_model, reservation_ip):
        logger.warning('update_reservation')
        drp_object = convert_to_drp(reservation_config_model)
        drp_object = self.session.put('reservations', drp_object, reservation_ip)
        reservation_model = convert_to_client(drp_object)
        logger.warning('Updated ' + reservation_ip)
        return reservation_model

    def delete_reservation(self, reservation_ip):
        logger.warning('delete_reservation')
        result = self.session.delete('reservations', reservation_ip)
        logger.warning('Deleted ' + reservation_ip)
        return


# {
#   "Addr": "string",
#   "Description": "string",
#   "Documentation": "string",
#   "Duration": 0,
#   "NextServer": "string",
#   "Options": [
#     {
#       "Code": 0,
#       "Value": "string"
#     }
#   ],
#   "Scoped": true,
#   "Strategy": "string",
#   "Token": "string",
# }
def convert_to_drp(reservation_model):
    logger.warning('convert_to_drp')
    drp_object = {
        "Addr": reservation_model.ip,
        "Documentation": reservation_model.type,
        "Token": reservation_model.mac,
        "Description": reservation_model.name,
        "Strategy": 'MAC',
        "Scoped": True
    }
    logger.warning('Converted client to drp')
    logger.warning(drp_object)
    return drp_object


def convert_to_client(drp_object):
    logger.warning(drp_object)
    reservation_model_dict = {
        'ip': drp_object.get('Addr'),
        'mac': drp_object.get('Token'),
        'name': drp_object.get('Description'),
        'type': drp_object.get('Documentation'),


        'available': drp_object.get('Available'),
        'errors': drp_object.get('Errors'),
        'read_only': drp_object.get('ReadOnly'),
        'validated': drp_object.get('Validated'),
    }
    logger.warning('Converted drp to client')
    reservation_model = ReservationModel(**reservation_model_dict)
    logger.warning(reservation_model)
    return reservation_model


def get_all_reservations(session):
    logger.warning('get_all_reservations')
    try:
        result = session.get('reservations')
        logger.warning('Fetched all reservations')
        return result
    except AuthorizationError as error:
        logger.error(error)
        raise error
    except ConnectionError as error:
        logger.error(error)
        raise error
