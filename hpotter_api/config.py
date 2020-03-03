import logging
from yaml import safe_load

def load_config():
    config = {}
    # from os import getcwd, listdir
    # print(getcwd())
    # print(listdir())
    with open('config.yaml', 'r') as f:
        config = safe_load(f)
    return config

_config = load_config()

dbUrl = _config.get('dbUrl')
port = _config.get('port')
logging_format = _config.get('logging_format')