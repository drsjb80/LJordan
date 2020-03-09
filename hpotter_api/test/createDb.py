from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from yaml import safe_load
from os import chdir
from os.path import dirname, abspath

Base = declarative_base()

def load_tables_dict(pathToYaml):
    tablesDict = {}
    with open(pathToYaml, 'r') as f:
        tablesDict = safe_load(f)
    
    return tablesDict

def create_database():
    from hpotter_api.test.tables import Connections, ShellCommands, Credentials
    from ipaddress import ip_address

    moduleDir = dirname(abspath(__file__)) + '/'
    dbUrl = 'sqlite:///' + moduleDir + 'db.sqlite3'
    print('Attempting to create database with')
    print('  dbUrl: ' + dbUrl)

    engine = create_engine(dbUrl, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

    Base.query = db_session.query_property()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    tablesDict = load_tables_dict(moduleDir + 'tablesDict.yaml')
    for row in tablesDict['Connections']:
        conn = Connections(
            sourceIP = ip_address(row['sourceIP']),
            sourcePort = row['sourcePort'],
            destIP = ip_address(row['destIP']),
            destPort = row['destPort'],
            proto = row['proto']
        )
        db_session.add(conn)
    db_session.commit() # need IDs assigned to set relationships

    for row in tablesDict['ShellCommands']:
        cmd = ShellCommands(
            command = row['command'],
            connection = Connections.query.get(row['connections_id'])
        )
        db_session.add(cmd)
    
    for row in tablesDict['Credentials']:
        creds = Credentials(
            username = row['username'],
            password = row['password'],
            connection = Connections.query.get(row['connections_id'])
        )
        db_session.add(creds)

    db_session.commit()

if __name__ == '__main__':
    from createDb import create_database
    create_database()