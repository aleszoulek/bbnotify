import sys
import time
import urllib
import json
from datetime import datetime

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
                }
                # compatibility with new json api
                if ret[builder_name] == 'failure':
                    ret[builder_name]['results'] = 'failed'
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
                return data
            except:
                print >> sys.stderr, "Connecting to %s failed. Trying again in %s sec." % (self.url, self.CONNECTION_RETRY_TIMEOUT)
                time.sleep(self.CONNECTION_RETRY_TIMEOUT)

    def fetch_builders(self):
        return self._get_json()['builders']

    def fetch_lastbuilds(self, builder_name):
        return self._get_json('/builders/%s/builds/-1' % builder_name)


    def get_status(self):
        ret = {}
        for builder_name in self.fetch_builders():
            last_build = self.fetch_lastbuilds(builder_name)
            if not last_build:
                return self.empty_build_status()
            ret[builder_name] = {
                'number': last_build['number'],
                'start': datetime.fromtimestamp(last_build['times'][0]),
                'finished': datetime.fromtimestamp(last_build['times'][1]),
                'branch': last_build['sourceStamp']['branch'],
                'revision': last_build['sourceStamp']['revision'],
                'result': last_build['text'][0],
                'text': last_build['text'][1],
            }
        return ret

