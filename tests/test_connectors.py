import datetime
from StringIO import StringIO
from unittest import TestCase

from bbnotify import connectors


def urlopen_json_mock(url):
    from tests.server import json_output
    return StringIO(json_output.URLS[url])


class TestJsonConnector(TestCase):

    def setUp(self):
        self.orig_url_open = connectors.urllib.urlopen
        connectors.urllib.urlopen = urlopen_json_mock

    def tearDown(self):
        connectors.urllib.urlopen = self.orig_url_open

    def test_simple(self):
        json = connectors.Json('http://buildbot/json')
        self.assertEquals(
            json.get_status(),
            {
                'builderB': {
                    'text': 'project 2 test',
                    'number': 30,
                    'start': datetime.datetime(2010, 11, 24, 14, 57, 31, 566614),
                    'finished': datetime.datetime(2010, 11, 24, 14, 57, 43, 804476),
                    'result': 'failed',
                    'branch': None,
                    'revision': '565c4ceadfea6dabd80e615485e2b5b5418090e7'
                },
                'builderA': {
                    'text': 'project 1 test',
                    'number': 30,
                    'start': datetime.datetime(2010, 11, 24, 14, 57, 31, 566614),
                    'finished': datetime.datetime(2010, 11, 24, 14, 57, 43, 804476),
                    'result': 'failed',
                    'branch': None,
                    'revision': '565c4ceadfea6dabd80e615485e2b5b5418090e7'
                },
            }
        )

