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

from enum import Enum
from drb_python.exceptions.http_exceptions import ConnectionError, \
    AuthorizationError


class ConnectionStatus(Enum):
    OPEN = 1
    CLOSED = 2
    ERROR = 3


class ApiHttp(object):
    """
    Base for All HTTP based API Calls
    """

    def __init__(self, session):
        self.session = session

    def connection_status(self):
        if self.session.is_authorized():
            return ConnectionStatus.OPEN
        else:
            return ConnectionStatus.CLOSED

    def open(self):
        try:
            if not self.session.is_authorized():
                self.session.authorize()
            return ConnectionStatus.OPEN
        except ConnectionError as error:
            raise error
        except AuthorizationError as error:
            raise error
