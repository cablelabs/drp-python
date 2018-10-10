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


class MachineModel(BaseModel):
    def __init__(self, **machine_object):
        super(MachineModel, self).__init__(**machine_object)
        self.ip = machine_object.get('ip')
        self.mac = machine_object.get('mac')
        self.name = machine_object.get('name')
        self.type = machine_object.get('type')
        self.os = machine_object.get('os')
        self.uuid = machine_object.get('uuid')
        self.workflow = machine_object.get('workflow')
        self.extension = machine_object.get('extension', {})
        self.available = machine_object.get('available')
        self.errors = machine_object.get('errors')
        self.read_only = machine_object.get('read_only')
        self.validated = machine_object.get('validated')
