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

import unittest

from drp_python.network_layer.http_session import HttpSession
from mock_server import MockServerRequestHandler
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] '
           '%(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger('drp-python')


class HttpSessionTest(unittest.TestCase):

    def setUp(self):
        self.mockServer = MockServerRequestHandler.setup_class()
        self.session = HttpSession('http://127.0.0.1:' +
                                   str(MockServerRequestHandler.mock_server_port),
                                   'username',
                                   'password')

    def tearDown(self):
        pass

    """
    Tests for functions located in HttpSession
    """
    def test_authorize(self):
        self.assertFalse(self.session.is_authorized())
        self.session.authorize()
        self.assertTrue(self.session.is_authorized())

    def test_get(self):
        self.session.authorize()
        self.assertTrue(self.session.is_authorized())
        data = self.session.get('/test', '1')
        self.assertEqual(data.get('Token'), '123')

    def test_post(self):
        self.session.authorize()
        self.assertTrue(self.session.is_authorized())
        data = self.session.post('test', {'Test': 'Data'})
        self.assertEqual(data['Test'], 'Data')

    def test_delete(self):
        self.session.authorize()
        self.assertTrue(self.session.is_authorized())
        data = self.session.delete('test', '1')
        self.assertEqual(data.get('Deleted'), '123')

    def test_put(self):
        self.session.authorize()
        self.assertTrue(self.session.is_authorized())
        data = self.session.put('test', {'Test': 'Data'}, '1')
        self.assertEqual(data['Test'], 'Data')
