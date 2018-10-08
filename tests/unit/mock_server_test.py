# import unittest
# from BaseHTTPServer import HTTPServer
# from mock_server import MockServerRequestHandler, get_free_port
# from threading import Thread
# import requests
#
#
# class TestMockServer(unittest.TestCase):
#     @classmethod
#     def setup_class(cls):
#         # Configure mock server.
#         cls.mock_server_port = get_free_port()
#         cls.mock_server = HTTPServer(('localhost', cls.mock_server_port),
#                                      MockServerRequestHandler)
#
#         # Start running mock server in a separate thread.
#         # Daemon threads automatically shut down when the main process exits.
#         cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
#         cls.mock_server_thread.setDaemon(True)
#         cls.mock_server_thread.start()
#
#     def test_request_response(self):
#         url = 'http://localhost:{port}/users'.format(
#             port=self.mock_server_port)
#         response = requests.get(url)
#         self.assertTrue(response.ok)
#
#         response = requests.post(url, {'test': '123'})
#         self.assertTrue(response.status_code == 201)
#
#         response = requests.put(url, {'test': '123'})
#         self.assertTrue(response.ok)
#
#         response = requests.delete(url)
#         self.assertTrue(response.status_code == 200)
#
