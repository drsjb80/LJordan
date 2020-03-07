import unittest

from os.path import dirname, abspath
from os import chdir

from hpotter_api.test.createDb import create_database
moduleDir = dirname(abspath(__file__)) + '/'
chdir(moduleDir)
create_database()
    
if __name__ == '__main__':

    import hpotter_api.test.test_schema as test_schema
    import hpotter_api.test.test_server as test_server

    suite = unittest.TestLoader().loadTestsFromModule(test_schema)
    unittest.TextTestRunner().run(suite)

    suite = unittest.TestLoader().loadTestsFromModule(test_server)
    unittest.TextTestRunner().run(suite)
    