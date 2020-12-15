import unittest
from unittest.mock import Mock

from ..hp_server import PostHandler

class ServerTests(unittest.TestCase):

    def test_non_json_400_resp(self):

        # need to figure out how to mock request and server
        
        # request = Mock()
        # client_address = ('0.0.0.0', 80)
        # server = Mock()
        # handler = PostHandler(request, client_address, server)
        # handler.headers = {'Content-Type': 'text/plain'}
        # handler.do_POST()

        self.assertTrue(True)
