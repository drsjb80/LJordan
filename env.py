# import logging
# import logging.config
# import platform
# import docker
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

# engine = create_engine(db)
# # engine = create_engine(db, echo=True)
# Base.metadata.create_all(engine)
# Session = scoped_session(sessionmaker(engine))

# a start, for a Pi 0.
# machine = 'arm32v6/' if platform.machine() == 'armv6l' else ''

# busybox = True
# shell_container = None

# def get_busybox():
#     return busybox

# def get_shell_container():
#     return shell_container

# def start_shell():
#     global shell_container
#     if shell_container:
#         logger.info('Shell container already started')
#         return

#     logger.info('Starting shell container')
#     client = docker.from_env()
#     if busybox:
#         shell_container = client.containers.run(machine + 'busybox:latest', \
#             command=['/bin/ash'], tty=True, detach=True, read_only=True)
#     else:
#         shell_container = client.containers.run(machine + 'alpine:latest', \
#             command=['/bin/ash'], user='guest', tty=True, detach=True, \
#                 read_only=True)

#     client.networks.get('bridge').disconnect(shell_container)

# def stop_shell():
#     if not shell_container:
#         return

#     logger.info('Stopping shell container')
#     shell_container.stop()
#     logger.info('Removing shell container')
#     shell_container.remove()



# some singletons
# telnet_server = None
# http500_server = None
# ssh_server_thread = None
