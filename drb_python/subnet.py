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

from http_exceptions import AuthorizationError, ConnectionError
from subnets_http import SubnetsHttp
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger('drb-python')


def create_subnet(session, **clientSubnet):
    subnet = Subnet(session, **clientSubnet)
    subnet.create()
    return subnet


class Subnet:
    """
    Client Subnet Object

    Args:
        session - Session object to connect to DRB
        clientSubnet:
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

    def __init__(self, session, **clientSubnet):
        logger.debug('__init__')
        self.client_obj = clientSubnet
        self.api = SubnetsHttp(session)

    def create(self):
        logger.debug('create')
        try:
            self.api.open()
            self.client_obj = self.api.create_subnet(**self.client_obj)
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def get(self):
        return self.client_obj

    def get_all(self):
        '''
        Fetches all subnets form DRP
        Note this data is not cached
        :return: Array of Subnets
        '''
        try:
            subnet_list = self.api.get_all_subnets()
            return subnet_list
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def fetch(self):
        try:
            self.client_obj = self.api.get_subnet(self.client_obj['name'])
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def update(self, **updated_object):
        try:
            self.client_obj = self.api.update_subnet(updated_object,
                                                     self.client_obj['name'])
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error

    def delete(self):
        try:
            self.api.delete_subnet(self.client_obj['name'])
        except ConnectionError as error:
            logger.error(error)
            raise error
        except AuthorizationError as error:
            logger.error(error)
            raise error
