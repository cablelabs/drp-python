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


import requests
import urllib3
from http_exceptions import AuthorizationError, ConnectionError
from drb_exceptions import AlreadyExists
urllib3.disable_warnings()


class HttpSession:
    def __init__(self, url, username, password, verify_cert=False):
        self.username = username
        self.password = password
        self.url = url
        self.token = ''
        self.verify_cert = verify_cert

    def authorize(self):
        try:
            r = requests.get(self.url + '/api/v3/users/rocketskates/token?ttl=28800',
                             auth=(self.username, self.password), verify=self.verify_cert)
            if r.status_code == 200:
                body = r.json()
                self.token = body['Token']
            elif r.status_code == 401 or r.status_code == 403:
                print 'Failed Authorizing ' + str(r.status_code) + ' '
                raise AuthorizationError(self.username + ', ' + self.password,
                                         'Failed To Authenticate with the Digital Rebar Server', r.status_code, r.text)
        except requests.ConnectionError as err:
                print 'Error Connecting to Digital Rebar Server'
                raise ConnectionError(self.url, 'Failed to Connect with the Digital Rebar Server',
                                      400, str(err.message))

    def is_authorized(self):
        return self.token != ''

    def get(self, resource, key=None):
        if not self.is_authorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actual_resource = resource
        if key is not None:
            actual_resource = actual_resource + '/' + key
        r = requests.get(self.url + '/api/v3/' + actual_resource, headers=headers, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            print 'Error on Get ' + str(r.status_code)
            print r.json()
            return r.status_code

    def post(self, resource, body):
        if not self.is_authorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actual_resource = resource
        print body
        r = requests.post(self.url + '/api/v3/' + actual_resource, headers=headers, json=body, verify=False)
        if r.status_code == 201:
            return r.json()
        else:
            print 'Error on Post ' + str(r.status_code)
            temp = r.json()
            raise AlreadyExists(body['Name'], str(temp['Messages'][0]))

    def delete(self, resource, key):
        if not self.is_authorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actual_resource = resource + '/' + key
        r = requests.delete(self.url + '/api/v3/' + actual_resource, headers=headers, verify=False)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            print 'Deleting a non-existant object, ignoring'
            return {}
        else:
            print 'Error on Delete ' + str(r.status_code)
            print r.json()
            return r.status_code

    def put(self, resource, body, key):
        if not self.is_authorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actual_resource = resource + '/' + key
        r = requests.post(self.url + '/api/v3/' + actual_resource, headers=headers, json=body, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            print 'Error on Put ' + str(r.status_code)
            print r.json()
            return r.status_code

