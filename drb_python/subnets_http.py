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
from http_exceptions import AuthorizationError, ConnectionError
from drb_exceptions import ActionError
from netaddr import IPAddress, IPNetwork


class SubnetsHttp(ApiHttp):
    """
     All HTTP based API Calls related to Subnets
    """

    def __init__(self, session):
        ApiHttp.__init__(self, session)
        self.drb_obj = None
        self.client_obj = None

    def get_all_subnets(self):
        try:
            result = self.session.get('subnets')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_subnet(self, subnet_name):
        try:
            self.drb_obj = self.session.get('subnets', subnet_name)
            self.convert_to_client()
            return self.client_obj
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def create_subnet(self, **subnet):
        try:
            self.client_obj = subnet
            self.convert_to_drb()
            self.drb_obj = self.session.post('subnets', self.drb_obj)
            self.convert_to_client()
            return self.client_obj
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def update_subnet(self, subnet, subnet_name):
        try:
            result = self.session.put('subnets', subnet, subnet_name)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def delete_subnet(self, subnet_name):
        try:
            result = self.session.delete('subnets', subnet_name)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_subnet_all_actions(self, subnet_name):
        try:
            result = self.session.get('subnets/' + subnet_name + '/actions')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_subnet_action(self, subnet_name, cmd):
        try:
            result = self.session.get('subnets/' + subnet_name + '/actions', cmd)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def execute_subnet_action(self, subnet_name, cmd):
        try:
            result = self.session.post('subnets/' + subnet_name + '/actions/' + cmd, {})
            if result == 400:
                raise ActionError(cmd, 'Action is not available on subnet ' + subnet_name)
            else:
                return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def convert_to_drb(self):
        """
        clientSubnet:
            address: "10.197.111.0"
            broadcast-address: "10.197.111.255"
            default-lease: 7600
            dn: cablelabs.com
            dns: "8.8.8.8"
            listen_iface: eno1
            max-lease: 7200
            name: Managment_SUBNET
            netmask: "255.255.255.0"
            range: "10.197.111.12 10.197.111.16"
            router: "10.197.111.1"
            type: management
             option option-128 code 128 = string;
            option option-129 code 129 = text;
            option vendor-class code 60 = string;
            option arch code 93 = unsigned integer 16;
            subnet 172.16.141.0 netmask 255.255.255.0{
              range 172.16.141.8 172.16.141.30;
              option domain-name-servers 10.203.171.38;
              option domain-name "aricentlabs.com";
              option subnet-mask 255.255.255.0;
              option routers 172.16.141.1;
              option broadcast-address 172.16.141.255;
              default-lease-time 7600;
              max-lease-time 7200;
              deny unknown-clients;
              }
        :return: 
        """
        print self.client_obj
        address = self.client_obj['address'] + '/' + str(IPAddress(self.client_obj['netmask']).netmask_bits())
        self.drb_obj = {
            "ActiveEnd": self.client_obj['range'].split(' ')[1],
            "ActiveLeaseTime": self.client_obj['default_lease'],
            "ActiveStart": self.client_obj['range'].split(' ')[0],
            "Description": self.client_obj['type'],
            "Enabled": True,
            "Name": self.client_obj['name'],
            "OnlyReservations": True,
            "Pickers": [
                "hint"
            ],
            "Proxy": False,
            "ReservedLeaseTime": self.client_obj['default_lease'],
            "Subnet": address,
            "Unmanaged": True,
            "Options": [
                {
                    "Code": 6,
                    "Value": self.client_obj['dns'],
                    'Description': 'Domain Name Server'
                },
                {
                    "Code": 15,
                    "Value": self.client_obj['dn'],
                    'Description': 'Domain Name'
                },
                {
                    "Code": 1,
                    "Value": self.client_obj['netmask'],
                    'Description': 'Network Mask'
                },
                {
                    "Code": 3,
                    "Value": self.client_obj['router'],
                    'Description': 'Router'
                },
                {
                    "Code": 28,
                    "Value": self.client_obj['broadcast_address'],
                    'Description': 'Broadcast Address'
                }

            ]
        }

    def convert_to_client(self):
        """
           "ActiveEnd": self.client_obj['range'].split(' ')[1],
        "ActiveLeaseTime": self.client_obj['default_lease'],
        "ActiveStart": self.client_obj['range'].split(' ')[0],
        "Description": self.client_obj['type'],
        "Enabled": True,
        "Name": self.client_obj['name'],
        "OnlyReservations": True,
        "Pickers": [
            "hint"
        ],
        "Proxy": False,
        "ReservedLeaseTime": self.client_obj['default_lease'],
        "Subnet": address,
        "Unmanaged": True,
        "Options": [
            {
                "Code": 6,
                "Value": self.client_obj['dns'],
                'Description': 'Domain Name Server'
            },
            {
                "Code": 15,
                "Value": self.client_obj['dn'],
                'Description': 'Domain Name'
            },
            {
                "Code": 1,
                "Value": self.client_obj['netmask'],
                'Description': 'Network Mask'
            },
            {
                "Code": 3,
                "Value": self.client_obj['router'],
                'Description': 'Router'
            },
            {
                "Code": 28,
                "Value": self.client_obj['broadcast_address'],
                'Description': 'Broadcast Address'
            }
        ]
        """
        ip = IPNetwork(str(self.drb_obj['Subnet']))
        address = str(ip.ip)
        netmask = str(ip.netmask)
        broadcast = str(ip.broadcast)
        self.client_obj = {
            'address': address,
            'broadcast_address': broadcast,
            'default_lease': self.drb_obj['ActiveLeaseTime'],
            'dn': self.drb_obj['Options'][1]['Value'],
            'dns': self.drb_obj['Options'][0]['Value'],
            'listen_iface': 'eno1',
            'max_lease': self.drb_obj['ReservedLeaseTime'],
            'name': self.drb_obj['Name'],
            'netmask': netmask,
            'range': self.drb_obj['ActiveStart'] + ' ' + self.drb_obj['ActiveEnd'],
            'router': self.drb_obj['Options'][3]['Value'],
            'type': self.drb_obj['Description']
        }
