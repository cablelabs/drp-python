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


class SubnetConfigModel(BaseModel):
    def __init__(self, **subnet_object):
        super(SubnetConfigModel, self).__init__(**subnet_object)
        self.address = subnet_object.get('address')
        self.broadcast_address = subnet_object.get('broadcast_address')
        self.default_lease = subnet_object.get('default_lease')
        self.dn = subnet_object.get('dn')
        self.dns = subnet_object.get('dns')
        self.listen_iface = subnet_object.get('listen_iface')
        self.max_lease = subnet_object.get('max_lease')
        self.name = subnet_object.get('name')
        self.netmask = subnet_object.get('netmask')
        self.range = subnet_object.get('range')
        self.router = subnet_object.get('router')
        self.type = subnet_object.get('type')
        self.unmanaged = subnet_object.get('unmanaged')
        self.pickers = subnet_object.get('pickers')
        self.extension = subnet_object.get('extension', {})
        if self.unmanaged is None:
            self.unmanaged = False
        if self.pickers is None:
            self.pickers = ['hint', 'nextFree', 'mostExpired']
