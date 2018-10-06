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

from drb_python.exceptions.http_exceptions import AuthorizationError, \
    ConnectionError
from drb_python.exceptions.drb_exceptions import NotFoundError, AlreadyExistsError
from drb_python.translation_layer.subnets_http import SubnetsHttp, \
    get_all_subnets
import logging

logger = logging.getLogger('drb-python')


class Subnet:
    """
    Client Subnet Object
    """
    def __init__(self, session, client_subnet):
        logger.debug('__init__')
        self.__subnet_config = client_subnet
        self.__api = SubnetsHttp(session)
        self.__api.open()
        try:
            self.__subnet_model = self.get()
        except NotFoundError:
            self.__subnet_model = None

    def is_valid(self):
        return self.__subnet_model is not None

    def create(self):
        logger.debug('create')
        if self.__subnet_model:
            raise AlreadyExistsError(self.__subnet_model.name,
                                     'Subnet with that name already exists')
        else:
            self.__subnet_model = self.__api.create_subnet(self.__subnet_config)

    def update(self, updated_object):
        if self.__subnet_model:
            self.__subnet_model = self.__api.update_subnet(updated_object,
                                                           self.__subnet_model.name)
        else:
            self.__subnet_model = self.__api.create_subnet(
                updated_object)

    def delete(self):
        if self.__subnet_model:
            self.__api.delete_subnet(self.__subnet_model.name)
            self.__subnet_model = None

    def get(self):
        return self.__api.get_subnet(self.__subnet_config.name)


def get_all(session):
    """
    Fetches all subnets form DRP
    Note this data is not cached
    :return: List of Subnets
    """
    try:
        subnet_list = get_all_subnets(session)
        return subnet_list
    except ConnectionError as error:
        logger.error(error)
        raise error
    except AuthorizationError as error:
        logger.error(error)
        raise error
