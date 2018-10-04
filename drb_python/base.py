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

from http_exceptions import AuthorizationError, ConnectionError
import abc


class Base(abc.ABCMeta):
    """
     Client Base class for interacting with DRP
    """

    def __init__(self, session):
        # type: (object) -> object
        self.host = 'https://10.197.113.130:8092'
        self.login = {'username': 'rocketskates', 'password': 'r0cketsk8ts'}
        self.object = None
        self.api = None
        self.session = session
        if config.has_key('host'):
            self.host = config.get('host')
        if config.has_key('login'):
            self.login = config.get('login')

    @abc.abstractmethod
    def create(self, **object):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass

    def get(self):
        return self.object

    @abc.abstractmethod
    def fetch(self):
        pass

    @abc.abstractmethod
    def update(self, **updated_object):
        pass

    @abc.abstractmethod
    def delete(self):
        pass
