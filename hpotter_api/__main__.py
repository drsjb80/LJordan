import logging
from os.path import dirname, abspath
from os import chdir

moduleDir = dirname(abspath(__file__)) + '/'
chdir(moduleDir)

if __name__ == '__main__':
    from .config import logging_format
    from .hp_server import serve_forever
    
    logging.basicConfig(format=logging_format, level=logging.DEBUG)
    logging.debug('Working dir set to %s', moduleDir)

    serve_forever()