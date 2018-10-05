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

from exceptions.http_exceptions import AuthorizationError, ConnectionError
from translation_layer.subnets_http import SubnetsHttp
import logging

logger = logging.getLogger('drb-python')


class Subnet:
    """
    Client Subnet Object

    Args:
        session - Session object to connect to DRB
        client_subnet:
            address: '10.197.111.0'
            broadcast-address: '10.197.111.255'
            default-lease: 7600
            dn: cablelabs.com
            dns: '8.8.8.8'
            listen_iface: eno1
            max-lease: 7200
            name: Managment_SUBNET
            netmask: '255.255.255.0'
            range: '10.197.111.12 10.197.111.16'
            router: '10.197.111.1'
            type: management

    """

    def __init__(self, session, **client_subnet):
        logger.debug('__init__')
        self.__subnet_model = client_subnet
        self.__api = SubnetsHttp(session)

    def create(self):
        logger.debug('create')
        try:
            self.__api.open()
            self.__subnet_model = self.__api.create_subnet(**self.__subnet_model)
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def get(self):
        return self.__subnet_model

    def refresh(self):
        try:
            self.__subnet_model = self.__api.get_subnet(self.__subnet_model['name'])
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def update(self, **updated_object):
        try:
            self.__subnet_model = self.__api.update_subnet(updated_object,
                                                     self.__subnet_model['name'])
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def delete(self):
        try:
            self.__api.delete_subnet(self.__subnet_model['name'])
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

def get_all(session):
    '''
    Fetches all subnets form DRP
    Note this data is not cached
    :return: List of Subnets
    '''
    try:
        subnet_list = SubnetsHttp.get_all_subnets(session)
        return subnet_list
    except ConnectionError as error:
        logger.error(error)
        raise error
    except AuthorizationError as error:
        logger.error(error)
        raise error