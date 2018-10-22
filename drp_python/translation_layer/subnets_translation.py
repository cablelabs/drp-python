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
from drp_python.model_layer.subnet_model import SubnetModel
from drp_python.exceptions.http_exceptions import AuthorizationError, \
    ConnectionError
from netaddr import IPAddress, IPNetwork
import logging

logger = logging.getLogger('drp-python')


class SubnetTranslation(ApiHttp):
    """
     All HTTP based API Calls related to Subnets
    """

    def __init__(self, session):
        super(SubnetTranslation, self).__init__(session)
        logger.debug('__init__')

    def get_subnet(self, subnet_name):
        logger.debug('get_subnet')
        drp_obj = self.session.get('subnets', subnet_name)
        subnet_model = convert_to_client(drp_obj)
        return subnet_model

    def create_subnet(self, subnet_config_model):
        logger.debug('create_subnet')
        drp_object = convert_to_drp(subnet_config_model)
        drp_object = self.session.post('subnets', drp_object)
        subnet_model = convert_to_client(drp_object)
        logger.info('Created ' + subnet_model.name)
        return subnet_model

    def update_subnet(self, subnet_config_model, subnet_name):
        logger.debug('update_subnet')
        drp_object = convert_to_drp(subnet_config_model)
        drp_object = self.session.put('subnets', drp_object, subnet_name)
        subnet_model = convert_to_client(drp_object)
        logger.info('Updated ' + subnet_name)
        return subnet_model

    def delete_subnet(self, subnet_name):
        logger.debug('delete_subnet')
        result = self.session.delete('subnets', subnet_name)
        logger.info('Deleted ' + subnet_name)
        return


def convert_to_drp(subnet_model):
    logger.debug('convert_to_drp')
    address = subnet_model.address + '/' + str(
        IPAddress(subnet_model.netmask).netmask_bits())
    print subnet_model.range
    drp_object = {
        "ActiveEnd": subnet_model.range.split(' ')[1],
        "ActiveLeaseTime": subnet_model.default_lease,
        "ActiveStart": subnet_model.range.split(' ')[0],
        "Description": subnet_model.type,
        "Enabled": True,
        "Name": subnet_model.name,
        "OnlyReservations": True,
        "Pickers": [
            "hint",
            "nextFree",
            "mostExpired"
        ],
        "Strategy": "MAC",
        "Proxy": False,
        "ReservedLeaseTime": subnet_model.default_lease,
        "Subnet": address,
        "Unmanaged": False,
        "Options": [
            {
                "Code": 6,
                "Value": subnet_model.dns
            },
            {
                "Code": 15,
                "Value": subnet_model.dn
            },
            {
                "Code": 1,
                "Value": subnet_model.netmask
            },
            {
                "Code": 3,
                "Value": subnet_model.router
            },
            {
                "Code": 28,
                "Value": subnet_model.broadcast_address
            }

        ]
    }
    logger.info('Converted client to drp')
    logger.info(drp_object)
    return drp_object


def convert_to_client(drp_object):
    logger.warn(drp_object)
    ip = IPNetwork(str(drp_object.get('Subnet')))
    address = str(ip.ip)
    netmask = str(ip.netmask)
    broadcast = str(ip.broadcast)
    subnet_model_dict = {
        'address': address,
        'broadcast_address': broadcast,
        'default_lease': drp_object.get('ActiveLeaseTime'),
        'dn': drp_object.get('Options')[1].get('Value'),
        'dns': drp_object.get('Options')[0].get('Value'),
        'listen_iface': 'eno1',
        'max_lease': drp_object.get('ReservedLeaseTime'),
        'name': drp_object.get('Name'),
        'netmask': netmask,
        'range': drp_object.get('ActiveStart') + ' ' + drp_object.get(
            'ActiveEnd'),
        'router': drp_object.get('Options')[3].get('Value'),
        'type': drp_object.get('Description'),

        'available': drp_object.get('Available'),
        'errors': drp_object.get('Errors'),
        'validated': drp_object.get('Validated'),
        'read_only': drp_object.get('ReadOnly'),
        'options': drp_object.get('Options'),
        'pickers': drp_object.get('Pickers'),
        'strategy': drp_object.get('Strategy')
    }
    logger.info('Converted drp to client')
    subnet_model = SubnetModel(**subnet_model_dict)
    logger.info(subnet_model)
    return subnet_model


def get_all_subnets(session):
    logger.debug('get_all_subnets')
    try:
        result = session.get('subnets')
        logger.info('Fetched all subnets')
        return result
    except AuthorizationError as error:
        logger.error(error)
        raise error
    except ConnectionError as error:
        logger.error(error)
        raise error
