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
from uuid import uuid1
from translation_layer.machines_http import MachinesHttp
from exceptions.drb_exceptions import AlreadyExistsError
import logging

logger = logging.getLogger('drb-python')


def create_machine(session, client_machine):
    machine = Machine(session, client_machine)
    machine.create()
    return machine


class Machine():
    """
     Client Machine class for interacting with DRP
    """
    def __init__(self, session, **client_machine):
        logger.debug('__init__')
        self.client_obj = client_machine
        self.api = MachinesHttp(session)
        self.client_obj['uuid'] = uuid1()

    def create(self):
        logger.debug('create')
        try:
            self.api.open()
            self.client_obj = self.api.create_machine(**self.client_obj)
            return True
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error
        except AlreadyExistsError as error:
            logger.error(error)
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
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def get(self):
        return self.client_obj

    def fetch(self):
        try:
            self.client_obj = self.api.get_machine(self.client_obj['uuid'])
            return True
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def update(self, **updated_object):
        try:
            self.client_obj = self.api.update_machine(updated_object, self.client_obj['uuid'])
            return True
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def delete(self):
        try:
            self.api.delete_machine(self.client_obj['uuid'])
            return True
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error
