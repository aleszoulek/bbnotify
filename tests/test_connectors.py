import datetime

from tests.helpers import TestCase
from bbnotify import connectors


class TestJsonConnector(TestCase):

    mock_json = True

    def test_simple(self):
        json = connectors.Json('http://buildbot/json')
        self.assertEquals(
            json.get_status(),
            {
                'failingBuilderB': {
                    'text': 'project 2 test',
                    'number': 30,
                    'start': datetime.datetime(2010, 11, 24, 14, 57, 31, 566614),
                    'finished': datetime.datetime(2010, 11, 24, 14, 57, 43, 804476),
                    'result': 'failed',
                    'branch': None,
                    'revision': '565c4ceadfea6dabd80e615485e2b5b5418090e7'
                },
                'failingBuilderA': {
                    'text': 'project 1 test',
                    'number': 30,
                    'start': datetime.datetime(2010, 11, 24, 14, 57, 31, 566614),
                    'finished': datetime.datetime(2010, 11, 24, 14, 57, 43, 804476),
                    'result': 'failed',
                    'branch': None,
                    'revision': '565c4ceadfea6dabd80e615485e2b5b5418090e7'
                },
                'passingBuilderX': {
                    'text': 'successful',
                    'number': 13,
                    'start': datetime.datetime(2010, 11, 24, 22, 1, 10, 720937),
                    'finished': datetime.datetime(2010, 11, 24, 22, 8, 23, 109146),
                    'result': 'successful',
                    'branch': '1.2.X',
                    'revision': '14695',
                },
            }
        )

    def test_include_ignore(self):
        json = connectors.Json('http://buildbot/json', ignore=['failingBuilderB'])
        self.assertEquals(set(json.get_status().keys()), set(['failingBuilderA', 'passingBuilderX']))
        json = connectors.Json('http://buildbot/json', include=['failingBuilderB'])
        self.assertEquals(json.get_status().keys(), ['failingBuilderB'])
        json = connectors.Json('http://buildbot/json', include=['failingBuilderB'], ignore=['failingBuilderA'])
        self.assertEquals(json.get_status().keys(), ['failingBuilderB'])
        json = connectors.Json('http://buildbot/json', include=['failingBuilderB'], ignore=['failingBuilderB'])
        self.assertEquals(json.get_status().keys(), [])


class TestXmlRpcConnector(TestCase):

    mock_xmlrpc = True

    def test_status(self):
        xmlrpc = connectors.XmlRpc('http://buildbot/xmlrpc')
        self.maxDiff = None
        self.assertEquals(
            xmlrpc.get_status(),
            {
                'failingBuilderB': {
                    'text': 'project 2 test',
                    'number': 30,
                    'start': datetime.datetime(2010, 11, 24, 14, 57, 31, 566614),
                    'finished': datetime.datetime(2010, 11, 24, 14, 57, 43, 804476),
                    'result': 'failed',
                    'branch': None,
                    'revision': '565c4ceadfea6dabd80e615485e2b5b5418090e7'
                },
                'failingBuilderA': {
                    'text': 'project 1 test',
                    'number': 30,
                    'start': datetime.datetime(2010, 11, 24, 14, 57, 31, 566614),
                    'finished': datetime.datetime(2010, 11, 24, 14, 57, 43, 804476),
                    'result': 'failed',
                    'branch': None,
                    'revision': '565c4ceadfea6dabd80e615485e2b5b5418090e7'
                },
                'passingBuilderX': {
                    'text': 'successful',
                    'number': 13,
                    'start': datetime.datetime(2010, 11, 24, 22, 1, 10, 720937),
                    'finished': datetime.datetime(2010, 11, 24, 22, 8, 23, 109146),
                    'result': 'successful',
                    'branch': '1.2.X',
                    'revision': '14695',
                },
            }
        )

    def test_include_ignore(self):
        xmlrpc = connectors.XmlRpc('http://buildbot/xmlrpc', ignore=['failingBuilderB'])
        self.assertEquals(set(xmlrpc.get_status().keys()), set(['failingBuilderA', 'passingBuilderX']))
        xmlrpc = connectors.XmlRpc('http://buildbot/xmlrpc', include=['failingBuilderB'])
        self.assertEquals(xmlrpc.get_status().keys(), ['failingBuilderB'])
        xmlrpc = connectors.XmlRpc('http://buildbot/xmlrpc', include=['failingBuilderB'], ignore=['failingBuilderA'])
        self.assertEquals(xmlrpc.get_status().keys(), ['failingBuilderB'])
        xmlrpc = connectors.XmlRpc('http://buildbot/xmlrpc', include=['failingBuilderB'], ignore=['failingBuilderB'])
        self.assertEquals(xmlrpc.get_status().keys(), [])
