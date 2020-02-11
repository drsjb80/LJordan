from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy_utils import IPAddressType

# https://www.ietf.org/rfc/rfc1700.txt
TCP = 6
UDP = 17

Base = declarative_base()

class Connections(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    sourceIP = Column(IPAddressType)
    sourcePort = Column(Integer)
    destIP = Column(IPAddressType)
    destPort = Column(Integer)
    proto = Column(Integer)

class ShellCommands(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    command = Column(String)
    connections_id = Column(Integer, ForeignKey('connections.id'))
    connection = relationship('Connections')

class Credentials(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    connections_id = Column(Integer, ForeignKey('connections.id'))
    connection = relationship('Connections')

class HTTPCommands(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    request = Column(String)
    connections_id = Column(Integer, ForeignKey('connections.id'))
    connection = relationship('Connections')


class SQL(Base):
    # pylint: disable=E0213, R0903
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    request = Column(String)
    connections_id = Column(Integer, ForeignKey('connections.id'))
    connection = relationship('Connections')
