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
from base import Base


def createSubnet(session, **clientSubnet):
    subnet = Subnet(session, clientSubnet)
    subnet.create()
    return subnet


class Subnet(Base):
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
        super(Subnet, self).__init__(session, clientSubnet)
        self.address = clientSubnet.get('address')
        self.broadcast_address = clientSubnet.get('broadcast_address')
        self.default_lease = clientSubnet.get('default_lease')
        self.dn = clientSubnet.get('dn')
        self.dns =  clientSubnet.get('dns')
        self.listen_iface = clientSubnet.get('listen_iface')
        self.max_lease = clientSubnet.get('max_lease')
        self.name = clientSubnet.get('name')
        self.netmask = clientSubnet.get('netmask')
        self.range = clientSubnet.get('range')
        self.router = clientSubnet.get('router')
        self.type = clientSubnet.get('type')
        self.api = SubnetsHttp(self.session)

    def create(self):
        self.api.open()
        self.api.create_subnet(self.address, self.broadcast_address, self.default_lease, self.dn,
                                             self.dns, self.listen_iface, self.max_lease, self.name, self.netmask,
                                             self.range, self.router, self.type)

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
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def fetch(self):
        try:
            self.object = self.api.get_subnet(self.object.name)
            return self.object
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def update(self, **updated_object):
        try:
            self.object = self.api.update_subnet(updated_object, self.object.name)
            return self.object
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error

    def delete(self):
        try:
            self.object = self.api.delete_subnet(self.object.name)
            return self.object
        except ConnectionError as error:
            print error
            raise error
        except AuthorizationError as error:
            print error
            raise error
