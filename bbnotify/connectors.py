import sys
import time
import urllib
import json

from xmlrpclib import ServerProxy



class XmlRpc(object):

    CONNECTION_RETRY_TIMEOUT = 10

    def __init__(self, url):
        self.url = url
        self.connection = ServerProxy(self.url)
        self.last_status = {}

    def call(self, name, *args, **kwargs):
        while True:
            try:

                return getattr(self.connection, name)(*args, **kwargs)
            except:
                print >> sys.stderr, "Connecting to %s failed. Trying again in %s sec." % (self.url, self.CONNECTION_RETRY_TIMEOUT)
                time.sleep(self.CONNECTION_RETRY_TIMEOUT)

    def get_status(self):
        ret = {}
        for builder_name in self.call('getAllBuilders'):
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
                    'reasons': results[8],
                }
            else:
                #The builder has no build, use "nobuild" as it's status
                ret[builder_name] = {
                    'number': 0,
                    'start': datetime.today(),
                    'finished': datetime.today(),
                    'branch': '',
                    'revision': '0',
                    'result': 'nobuild',
                    'text': 'no current build',
                    'reasons': '',
                }
        return ret


class Json(object):

    def __init__(self, url):
        self.url = url
        self.last_status = {}

    def _get_json(self, path=''):
        while True:
            try:
                fp = urllib.urlopen("%s%s" % (self.url, path))
                data = json.loads(fp.read())
                fp.close()
                return data['builders']
            except:
                print >> sys.stderr, "Connecting to %s failed. Trying again in %s sec." % (self.url, self.CONNECTION_RETRY_TIMEOUT)
                time.sleep(self.CONNECTION_RETRY_TIMEOUT)

    def fetch_builders(self):
        return self._get_json()['builders']

    def fetch_lastbuilds(self, builder_name):
        return self._get_json('/builders/%s/builds/-1' % builder_name)


    def get_status(self):
        ret = {}
        data = self.fetch()
        for builder_name in self.fetch_builders():

