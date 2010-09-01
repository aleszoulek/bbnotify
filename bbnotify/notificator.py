#!/usr/bin/env python

import os
import gtk
import time
import gobject
import webbrowser
import urlparse

from os.path import join, dirname, abspath
from datetime import datetime
from xmlrpclib import ServerProxy



MEDIA_DIR = join(abspath(dirname(__file__)), 'media')
TIMEOUT = 1000 * 30


class BuildBot(object):

    def __init__(self, url):
        self.url = url
        self.connection = ServerProxy(self.url)
        self.last_status = {}

    def get_status(self):
        ret = {}
        for builder_name in self.connection.getAllBuilders():
            results = self.connection.getLastBuilds(builder_name, 3)[-1]
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
        return ret


class Notificator(object):
    ICONS = {
        'success': 'green.png',
        'failure': 'red.png',
    }

    def __init__(self, url):
        self.buildbot = BuildBot(url)
        self.url = url
        self.icons = {}
        self.statuses = {}
        self.start()

    def refresh(self):
        for name, status in self.buildbot.get_status().items():
            if name not in self.icons:
                self.icons[name] = gtk.StatusIcon()
                self.icons[name].connect("activate", self.on_left_click)
            self.icons[name].set_from_file(join(MEDIA_DIR, self.ICONS.get(status['result'])))
            self.icons[name].set_tooltip(name)
            if name in self.statuses:
                if self.statuses[name]['finished'] < status['finished']:
                    try:
                        os.popen(
                            'notify-send -u %s -t 10000 "BuildBot" "%s: New build finished"' %
                            (
                                status['result'] == 'success' and 'normal' or 'critical',
                                name,
                            )
                        )
                    except:
                        pass
            self.statuses[name] = status
        return True
        
    def on_left_click(self, status_icon):
        url = urlparse.urlparse(self.url)
        waterfall = "%s://%s/waterfall" % (url.scheme, url.netloc)
        webbrowser.open(waterfall)
        
    def start(self):
        self.refresh()
        gobject.timeout_add(TIMEOUT, self.refresh)

