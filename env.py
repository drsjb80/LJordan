# import logging
# import logging.config
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from hpotter.tables import Base

# logging.config.fileConfig('hpotter/logging.conf')
# logger = logging.getLogger('hpotter')

# note sqlite:///:memory: can't be used, even for testing, as it
# doesn't work with threads.
uriScheme = 'sqlite:///'
dbPath = '../HPotter/main.db'
jsonserverport = 8000

#     logger.info('Starting shell container')
