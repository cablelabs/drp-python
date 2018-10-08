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
from drp_python.exceptions.http_exceptions import AuthorizationError, ConnectionError
from netaddr import IPAddress, IPNetwork
import logging

logger = logging.getLogger('drp-python')


class MachinesHttp(ApiHttp):
    """
     All HTTP based API Calls related to Machines
    """

    def __init__(self, session):
        super(MachinesHttp, self).__init__(session)
        logger.debug('__init__')
        self.drb_obj = None
        self.client_obj = None

    def get_all_machines(self):
        logger.debug('get_all_machines')
        try:
            result = self.session.get('machines')
            logger.info('Fetched all machines')
            return result
        except AuthorizationError as error:
            logger.error(error)
            raise error
        except ConnectionError as error:
            logger.error(error)
            raise error

    def get_machine(self, uuid):
        logger.debug('get_machine')
        try:
            self.drb_obj = self.session.get('machines', uuid)
            self.convert_to_client()
            logger.info('Got cached ' + uuid)
            return self.client_obj
        except AuthorizationError as error:
            logger.error(error)
            raise error
        except ConnectionError as error:
            logger.error(error)
            raise error

    def create_machine(self, **machine):
        logger.debug('create_machine')
        try:
            self.client_obj = machine
            self.convert_to_drb()
            self.drb_obj = self.session.post('machines', machine)
            self.convert_to_client()
            logger.info('Created ' + self.client_obj['name'])
            return self.client_obj
        except AuthorizationError as error:
            logger.error(error)
            raise error
        except ConnectionError as error:
            logger.error(error)
            raise error

    def update_machine(self, machine, uuid):
        logger.debug('update_machine')
        try:
            self.client_obj = machine
            self.convert_to_drb()
            self.client_obj = self.session.put('machines', self.drb_obj, uuid)
            self.convert_to_client()
            logger.info('Updated ' + uuid)
            return self.client_obj
        except AuthorizationError as error:
            logger.error(error)
            raise error
        except ConnectionError as error:
            logger.error(error)
            raise error

    def delete_machine(self, uuid):
        logger.debug('delete_machine')
        try:
            result = self.session.delete('machines', uuid)
            logger.info('Deleted ' + uuid)
            return result
        except AuthorizationError as error:
            logger.error(error)
            raise error
        except ConnectionError as error:
            logger.error(error)
            raise error

    def convert_to_drb(self):
        logger.debug('convert_to_drb')
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
        """
        self.drb_obj = {
            "Address": self.client_obj['address'],
            "BootEnv": self.client_obj['boot_env'],
            "Description": self.client_obj['description'],
            "HardwareAddrs": [
                self.client_obj['mac']
            ],
            "Name": self.client_obj['name'],
            "OS": self.client_obj['os'],
            "Runnable": True,
            "Uuid": self.client_obj['uuid'],
            "Workflow": self.client_obj['workflow']
        }
        logger.info('Converted client to drb')
        logger.info(self.drb_obj)

    def convert_to_client(self):
        """
            Converts DRP format to SubnetModel
        """
        self.client_obj = {
            'address': self.drb_obj['address'],
            'boot_env': self.drb_obj['BootEnv'],
            'description': self.drb_obj['Description'],
            'mac': self.drb_obj['HardwareAddrs'][0],
            'name': self.drb_obj['Name'],
            'os': self.drb_obj['OS'],
            'uuid': self.drb_obj['Uuid'],
            'workflow': self.drb_obj['Workflow']
        }
        logger.info('Converted drb to client')
        logger.info(self.client_obj)

    # def get_all_machines_params(self):
    #     try:
    #         result = self.httpProxy.get('machines')
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def get_machine_params(self, uuid):
    #     try:
    #         result = self.httpProxy.get('machines', uuid)
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def create_machine_params(self, uuid, param):
    #     try:
    #         result = self.httpProxy.post('machines'/ + uuid + '/params', param)
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def create_single_machine_param(self, uuid, key, param):
    #     try:
    #         result = self.httpProxy.post('machines'/ + uuid + '/params/' + key, param)
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def delete_machine_params(self, uuid):
    #     try:
    #         result = self.httpProxy.delete('machines', uuid)
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def get_machine_all_actions(self, uuid):
    #     try:
    #         result = self.httpProxy.get('machines/' + uuid + '/actions')
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    #
    # def get_machine_action(self, uuid, cmd):
    #     try:
    #         result = self.httpProxy.get('machines/' + uuid + '/actions', cmd)
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def execute_machine_action(self, uuid, cmd):
    #     try:
    #         result = self.httpProxy.post('machines/' + uuid + '/actions/' + cmd, {})
    #         if result == 400:
    #             raise ActionError(cmd, 'Action is not available on machine ' + uuid)
    #         else:
    #             return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
    #
    # def get_machine_pubkey(self, uuid):
    #     try:
    #         result = self.httpProxy.get('machines/' + uuid + '/pubkey')
    #         return result
    #     except AuthorizationError as error:
    #         print error
    #         raise error
    #     except ConnectionError as error:
    #         print error
    #         raise error
