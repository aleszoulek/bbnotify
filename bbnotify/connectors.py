import sys
import time
import urllib
import json
from datetime import datetime

from xmlrpclib import ServerProxy


class BaseConnector(object):

    CONNECTION_RETRY_TIMEOUT = 10

    def __init__(self, url, ignore=None, include=None):
        self.url = url
        self.ignore = ignore
        self.include = include

    def call(self, *args, **kwargs):
        while True:
            try:
                return self.query(*args, **kwargs)
            except:
                print >> sys.stderr, "Connecting to %s failed. Trying again in %s sec." % (
                    self.url,
                    self.CONNECTION_RETRY_TIMEOUT
                )
                time.sleep(self.CONNECTION_RETRY_TIMEOUT)

    def empty_build_status(self):
        return {
            'number': 0,
            'start': datetime.today(),
            'finished': datetime.today(),
            'branch': '',
            'revision': '0',
            'result': 'nobuild',
            'text': 'no current build',
        }

    def get_builders(self):
        builders = self.fetch_builders()
        if self.ignore:
            builders = [b for b in builders if b not in self.ignore]
        if self.include:
            builders = [b for b in builders if b in self.include]
        return builders


class XmlRpc(BaseConnector):

    def __init__(self, url, *args, **kwargs):
        super(XmlRpc, self).__init__(url, *args, **kwargs)
        self.connection = ServerProxy(self.url)
        self.last_status = {}

    def query(self, name, *args, **kwargs):
        return getattr(self.connection, name)(*args, **kwargs)

    def fetch_builders(self):
        return self.call('getAllBuilders')

    def get_status(self):
        ret = {}
        for builder_name in self.get_builders():
            lastbuilds = self.call('getLastBuilds', builder_name, 3)
            if len(lastbuilds) > 0:
                results = lastbuilds[-1]
                ret[builder_name] = {
                    'number': results[1],
                    'start': datetime.fromtimestamp(results[2]),
                    'finished': datetime.fromtimestamp(results[3]),
                    'branch': results[4],
                    'revision': results[5],
                    'result': results[6],
                    'text': results[7],
                }
                # compatibility with new json api
                if ret[builder_name]['result'] == 'success':
                    ret[builder_name]['result'] = 'successful'
                if ret[builder_name]['result'] == 'failure':
                    ret[builder_name]['result'] = 'failed'
            else:
                ret[builder_name] = self.empty_build_status()
        return ret


class Json(BaseConnector):

    def query(self, path=''):
        fp = urllib.urlopen("%s%s" % (self.url, path))
        data = json.loads(fp.read())
        fp.close()
        return data

    def fetch_builders(self):
        return self.call()['builders']

    def fetch_lastbuilds(self, builder_name):
        build = self.call('/builders/%s/builds/-1' % builder_name)
        if build and build['times'][1] is None:
            return self.call('/builders/%s/builds/-2' % builder_name)
        return build

    def parse_result(self, data):
        if 'successful' in data['text']:
            return 'successful'
        return 'failed'

    def get_status(self):
        ret = {}
        for builder_name in self.get_builders():
            last_build = self.fetch_lastbuilds(builder_name)
            if not last_build:
                ret[builder_name] = self.empty_build_status()
            else:
                ret[builder_name] = {
                    'number': last_build['number'],
                    'start': datetime.fromtimestamp(last_build['times'][0]),
                    'finished': datetime.fromtimestamp(last_build['times'][1]),
                    'branch': last_build['sourceStamp']['branch'],
                    'revision': last_build['sourceStamp']['revision'],
                    'result': self.parse_result(last_build),
                    'text': last_build['text'][1],
                }
        return ret

