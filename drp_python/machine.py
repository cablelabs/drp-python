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
from drp_python.translation_layer.machines_translation import \
    MachineTranslation, \
    get_all_machines
import logging

logger = logging.getLogger('drp-python')


class Machine:
    """
    Client Machine Object
    """

    def __init__(self, session, client_machine):
        logger.debug('__init__')
        self.__machine_config = client_machine
        self.__api = MachineTranslation(session)
        self.__api.open()
        try:
            self.__machine_model = self.get()
        except NotFoundError:
            self.__machine_model = None

    def is_valid(self):
        return self.__machine_model is not None

    def create(self):
        logger.debug('create')
        if self.__machine_model:
            raise AlreadyExistsError(self.__machine_model.name,
                                     'Machine with that name already exists')
        else:
            self.__machine_model = self.__api.create_machine(
                self.__machine_config)

    def update(self, updated_object):
        if self.__machine_model:
            self.__machine_model = self.__api.update_machine(
                updated_object, self.__machine_model.name)
        else:
            self.__machine_model = self.__api.create_machine(
                updated_object)

    def delete(self):
        if self.__machine_model:
            self.__api.delete_machine(self.__machine_model.uuid)
            self.__machine_model = None

    def get(self):
        if self.__machine_config.uuid is not None:
            return self.__api.get_machine(self.__machine_config.uuid)
        else:
            return self.__api.get_machine_by_name(self.__machine_config.name)


def get_all(session):
    """
    Fetches all machines form DRP
    Note this data is not cached
    :return: List of Machines
    """
    try:
        machine_list = get_all_machines(session)
        return machine_list
    except ConnectionError as error:
        logger.error(error)
        raise error
    except AuthorizationError as error:
        logger.error(error)
        raise error
