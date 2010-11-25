import unittest
from StringIO import StringIO

from bbnotify import connectors


def urlopen_json_mock(url):
    from tests.server import json_output
    return StringIO(json_output.URLS[url])


class MockServerProxy(object):
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        from tests.server import xmlrpc_methods
        if name in xmlrpc_methods.METHODS:
            return xmlrpc_methods.METHODS[name]
        return getattr(super(MockServerProxy, self), name)


class TestCase(unittest.TestCase):
    mock_xmlrpc = False
    mock_json = False

    def setUp(self):
        if self.mock_json:
            self.orig_url_open = connectors.urllib.urlopen
            connectors.urllib.urlopen = urlopen_json_mock
        if self.mock_xmlrpc:
            self.orig_server_proxy = connectors.ServerProxy
            connectors.ServerProxy = MockServerProxy

    def tearDown(self):
        if self.mock_json:
            connectors.urllib.urlopen = self.orig_url_open
        if self.mock_xmlrpc:
            connectors.ServerProxy = self.orig_server_proxy
