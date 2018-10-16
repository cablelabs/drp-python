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
from uuid import uuid4


# ip: "10.197.111.12"
# mac: "10:7d:1a:68:0d:2f"
# name: ADMIN_INTERFACE
# netmask: "255.255.255.0"
# range: "10.197.111.12 10.197.111.16"
# router: "10.197.111.1"
# type: management
class ReservationConfigModel(BaseModel):
    def __init__(self, **reservation_object):
        super(ReservationConfigModel, self).__init__(**reservation_object)
        self.ip = reservation_object.get('ip')
        self.mac = reservation_object.get('mac')
        self.name = reservation_object.get('name')
        self.netmask = reservation_object.get('netmask')
        self.gateway = reservation_object.get('gateway')
        self.type = reservation_object.get('type')

        self.extension = reservation_object.get('extension', {})
