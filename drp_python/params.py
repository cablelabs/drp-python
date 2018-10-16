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
from drp_python.translation_layer.params_translation import \
    ParamsTranslation, get_all_params
import logging

logger = logging.getLogger('drp-python')


class Params:
    """
    Client Params Object
    """

    def __init__(self, session, client_params):
        logger.debug('__init__')
        self.__params_config = client_params
        self.__api = ParamsTranslation(session)
        self.__api.open()
        try:
            self.__params_model = self.get()
        except NotFoundError:
            self.__params_model = None

    def is_valid(self):
        return self.__params_model is not None

    def create(self):
        logger.debug('create')
        if self.__params_model:
            raise AlreadyExistsError(self.__params_model.name,
                                     'Params with that name already exists')
        else:
            self.__params_model = self.__api.create_params(
                self.__params_config)

    def update(self, updated_object):
        if self.__params_model:
            self.__params_model = self.__api.update_params(
                updated_object, self.__params_model.name)
        else:
            self.__params_model = self.__api.create_params(
                updated_object)

    def delete(self):
        if self.__params_model:
            self.__api.delete_params(self.__params_model.name)
            self.__params_model = None

    def get(self):
        return self.__api.get_params(self.__params_config.name)

    def set_machine_param(self, machine):
        machine.add_param_values(self.__params_config)


def get_all(session):
    """
    Fetches all params form DRP
    Note this data is not cached
    :return: List of Params
    """
    try:
        params_list = get_all_params(session)
        return params_list
    except ConnectionError as error:
        logger.error(error)
        raise error
    except AuthorizationError as error:
        logger.error(error)
        raise error
