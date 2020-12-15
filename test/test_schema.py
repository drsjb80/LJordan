import unittest
from json import loads, dumps

from ..schema import schema

class SchemaTests(unittest.TestCase):

    def test_query_all_connections(self):
        postBody = r'{"query":"{\n  allConnections{\n    edges{\n      node{\n        destIP\n        destPort\n        sourceIP\n        sourcePort\n      }\n    }\n  }\n}","variables":null,"operationName":null}'
        query = loads(postBody)['query']
        result = schema.execute(query).to_dict()

        data = result.get('data')
        self.assertIsNotNone(data)
        allConnections = data.get('allConnections')
        self.assertIsNotNone(allConnections)
        edges = allConnections.get('edges')
        self.assertIsNotNone(edges)
        self.assertTrue(len(edges) == 2)

        expectedJson = r'{"data": {"allConnections": {"edges": [{"node": {"destIP": "127.0.0.1", "destPort": 80, "sourceIP": "127.0.0.1", "sourcePort": 80}}, {"node": {"destIP": "127.0.0.2", "destPort": 8080, "sourceIP": "127.0.0.2", "sourcePort": 8080}}]}}}'
        expectedResult = loads(expectedJson)
        self.assertDictContainsSubset(result, expectedResult)
    
    def test_query_creds_w_relationship(self):
        postBody = r'{"query":"{\n  allCredentials {\n    edges {\n      node {\n        username\n        password\n        connections {\n          id\n          destIP\n          destPort\n        }\n      }\n    }\n  }\n}\n","variables":null,"operationName":null}'
        query = loads(postBody)['query']
        result = schema.execute(query).to_dict()

        data = result.get('data')
        self.assertIsNotNone(data)
        allConnections = data.get('allCredentials')
        self.assertIsNotNone(allConnections)
        edges = allConnections.get('edges')
        self.assertIsNotNone(edges)
        self.assertTrue(len(edges) == 2)

        nodeContents = edges[0]['node']
        self.assertIsNotNone(nodeContents.get('connections'))

        expectedJson = r'{"data": {"allCredentials": {"edges": [{"node": {"username": "darth", "password": "theForceIsWrongWithThisOne", "connections": {"id": "Q29ubmVjdGlvbnNHcWw6MQ==", "destIP": "127.0.0.1", "destPort": 80}}}, {"node": {"username": "voldemort", "password": "scaredOnTheInside", "connections": {"id": "Q29ubmVjdGlvbnNHcWw6Mg==", "destIP": "127.0.0.2", "destPort": 8080}}}]}}}'
        expectedResult = loads(expectedJson)
        self.assertDictContainsSubset(result, expectedResult)