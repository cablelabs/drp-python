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

from base_model import BaseModel


class ParamsConfigModel(BaseModel):
    def __init__(self, **params_object):
        super(ParamsConfigModel, self).__init__(**params_object)
        self.name = params_object.get('name')
        self.value = params_object.get('value')
        self.schema = params_object.get('schema')
        self.type = params_object.get('type')
        self.description = params_object.get('description')

        self.extension = params_object.get('extension', {})
