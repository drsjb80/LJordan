import datetime
import decimal
import json
import os
import ipaddress

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from geolite2 import geolite2

from hpotter.env import db, jsonserverport
from hpotter.tables import Base, Connections

# http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/

engine = create_engine(db) #, echo=True)
session = sessionmaker(bind=engine)
session = session()
# magic to get all the tables.
Base.metadata.reflect(bind=engine)

def minutes_ago(diff):
    return datetime.datetime.utcnow() - datetime.timedelta(minutes=diff)

def hours_ago(diff):
    return datetime.datetime.utcnow() - datetime.timedelta(hours=diff)

def days_ago(diff):
    return datetime.datetime.utcnow() - datetime.timedelta(days=diff)

def weeks_ago(diff):
    return datetime.datetime.utcnow() - datetime.timedelta(weeks=diff)

def months_ago(diff):
    # a bit of an approximation
    return weeks_ago(diff*4)

def years_ago(diff):
    return weeks_ago(diff*52)

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()

    if isinstance(obj, decimal.Decimal):
        return float(obj)

    if isinstance(obj, ipaddress.IPv4Address):
        return str(obj)

    if isinstance(obj, ipaddress.IPv6Address):
        return str(obj)

class JSONHandler(SimpleHTTPRequestHandler):

    # this is for https://datatables.net/ and
    # https://github.com/daleroy1/freeboard-table
    def header_and_data(self, database, res):
        header = [column.name for column in database.columns]
        data = [dict(row) for row in res]
        dump = json.dumps({"header": header, "data": data}).encode('utf-8')
        self.wfile.write(dump)

    def geoip_results(self, results):
        reader = geolite2.reader()
        previous = False
        coordinates = []

        for result in results:
            info = reader.get(str(result[0])) or {}
            location = info.get('location', None)
            if not location:
                continue
            coordinate = []
            coordinates.append(
                [float(location['longitude']), float(location['latitude'])]
            )

        data = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint", 
                "coordinates": coordinates
            }
        }

        dump = json.dumps(data).encode('utf-8')
        self.wfile.write(dump)

    # https://tools.ietf.org/html/rfc7946#appendix-A.4
    def geoip(self):
        query = Connections.sourceIP
        # this order on the assumption there are fewer queries than deltas
        for delta in self.queries:
            if delta in self.deltas:
                diff = int(self.queries[delta][0])
                results = session.query(query) \
                    .filter(Connections.created_at > self.deltas[delta](diff)) \
                    .distinct()
                break
        else:
            results = session.query(query).distinct()

        self.geoip_results(results)

    def send_headers(self):
        self.send_response(200)
        if 'callback' in self.queries:
            mime = 'application/javascript'
        else:
            mime = 'text/javascript'
        self.send_header('Content-type', mime)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # pylint: disable=C0103
    def do_GET(self):
        url = urlparse(self.path)
        if url.path.endswith('.html'):
            SimpleHTTPRequestHandler.do_GET(self)
            return

        tables = Base.metadata.tables
        table_name = url.path[1:]

        if table_name in tables.keys():
            database = tables[table_name]
        else:
            self.send_response(404)
            return

        # here, so as not to override __init__
        # pylint: disable=W0201
        self.queries = {}
        if url.query:
            self.queries = parse_qs(url.query)

        self.send_headers()

        # here, so as not to override __init__
        # pylint: disable=W0201
        self.deltas = { \
            'minutes_ago':  minutes_ago, \
            'hours_ago':    hours_ago, \
            'days_ago':     days_ago, \
            'weeks_ago':    weeks_ago, \
            'months_ago':   months_ago, \
            'years_ago':    years_ago \
        }

        if table_name == 'connections' and 'geoip' in self.queries:
            self.geoip()
            return

        query = select([database])

        for delta in self.deltas:
            if delta in self.queries:
                diff = int(self.queries[delta][0])
                query = session.query(database).join(Connections) \
                    .filter(Connections.created_at > self.deltas[delta](diff))
                break

        results = session.execute(query)

        if 'handd' in self.queries:
            self.header_and_data(database, results)
            return

        dump = json.dumps([dict(r) for r in results], default=alchemyencoder)

        # JSONP
        if 'callback' in self.queries:
            self.wfile.write(self.queries['callback'][0].encode() + b'(')
            self.wfile.write(dump[1:-1].encode())
            self.wfile.write(b')')
        else:
            self.wfile.write(dump.encode())

try:
    os.chdir('hpotter/dashboard')
    server = HTTPServer(('', jsonserverport), JSONHandler)
    server.serve_forever()

except KeyboardInterrupt:
    print('Shutting down the web server')
    server.socket.close()
