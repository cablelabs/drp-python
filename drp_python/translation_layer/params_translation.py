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
from drp_python.exceptions.http_exceptions import AuthorizationError, \
    ConnectionError
from drp_python.model_layer.params_model import ParamsModel
import logging

logger = logging.getLogger('drp-python')


class ParamsTranslation(ApiHttp):
    """
     All HTTP based API Calls related to Params
    """

    def __init__(self, session):
        super(ParamsTranslation, self).__init__(session)
        logger.info('__init__')

    def get_params(self, params_name):
        logger.info('get_params')
        drp_obj = self.session.get('params', params_name)
        params_model = convert_to_client(drp_obj)
        return params_model

    def create_params(self, params_config_model):
        logger.info('create_params')
        drp_object = convert_to_drp(params_config_model)
        drp_object = self.session.post('params', drp_object)
        params_model = convert_to_client(drp_object)
        logger.info('Created ' + params_model.name)
        return params_model

    def update_params(self, params_config_model, params_name):
        logger.info('update_params')
        drp_object = convert_to_drp(params_config_model)
        drp_object = self.session.put('params', drp_object, params_name)
        params_model = convert_to_client(drp_object)
        logger.info('Updated ' + params_name)
        return params_model

    def delete_params(self, params_name):
        logger.info('delete_params')
        result = self.session.delete('params', params_name)
        logger.info('Deleted ' + params_name)
        return


def convert_to_drp(params_model):
    logger.info('convert_to_drp')
    drp_object = {
        "Name": params_model.name,
        "Description": params_model.type,
        "Schema": params_model.schema,
        "Documentation": params_model.description,
    }
    logger.info('Converted client to drp')
    logger.info(drp_object)
    return drp_object


def convert_to_client(drp_object):
    logger.info(drp_object)
    params_model_dict = {
        'name': drp_object.get('Name'),
        'schema': drp_object.get('Schema'),
        'type': drp_object.get('Description'),
        'description': drp_object.get('Documentation'),

        'available': drp_object.get('Available'),
        'errors': drp_object.get('Errors'),
        'read_only': drp_object.get('ReadOnly'),
        'validated': drp_object.get('Validated'),
    }
    logger.info('Converted drp to client')
    params_model = ParamsModel(**params_model_dict)
    logger.info(params_model)
    return params_model


def get_all_params(session):
    logger.info('get_all_params')
    try:
        result = session.get('params')
        logger.info('Fetched all params')
        return result
    except AuthorizationError as error:
        logger.error(error)
        raise error
    except ConnectionError as error:
        logger.error(error)
        raise error
