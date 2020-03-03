import unittest

from os.path import dirname, abspath
from os import chdir

moduleDir = dirname(abspath(__file__)) + '/'
chdir(moduleDir)

from hpotter_api.test.createDb import create_database
import hpotter_api.test.test_schema as test_schema
import hpotter_api.test.test_server as test_server

if __name__ == '__main__':
    create_database()
    suite = unittest.TestLoader().loadTestsFromModule(test_schema)
    unittest.TextTestRunner().run(suite)

    suite = unittest.TestLoader().loadTestsFromModule(test_server)
    unittest.TextTestRunner().run(suite)
    