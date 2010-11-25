#!/usr/bin/env python

import os
import gtk
import gobject
import webbrowser
import urlparse

from os.path import join, dirname, abspath

from bbnotify.connectors import XmlRpc, Json


MEDIA_DIR = join(abspath(dirname(__file__)), 'media')
TIMEOUT = 1000 * 30 # 30 sec

PROTOCOLS = {
    'xmlrpc': XmlRpc,
    'json': Json,
}



class Notificator(object):
    ICONS = {
        'successful': 'green.png',
        'failed': 'red.png',
        'nobuild': 'grey.png',
        'retry': 'grey.png',
        'exception': 'red.png',
        'partial': 'redgreen.png',
    }

    def __init__(self, url, ignore_builders, include_builders, protocol, group):
        if url.endswith('/'):
            url = url[:-1]
        self.url = url
        self.buildbot = PROTOCOLS[protocol](self.url, include=include_builders, ignore=ignore_builders)
        self.url = url
        self.group = group
        self.icons = {}
        self.statuses = {}
        self.start()

    def _refresh_icon(self, name, result):
        if name not in self.icons:
            self.icons[name] = gtk.StatusIcon()
            self.icons[name].connect("activate", self.on_left_click)
            self.icons[name].connect("popup-menu", self.on_right_click)
        self.icons[name].set_from_file(join(MEDIA_DIR, self.ICONS.get(result)))
        self.icons[name].set_tooltip(name)


    def _notify(self, name, status):
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

    def refresh(self):
        group_results = set([])
        for name, status in self.buildbot.get_status().items():
            self._notify(name, status)
            if self.group:
                group_results.add(status['result'])
            else:
                self._refresh_icon(name, status['result'])
            self.statuses[name] = status
        if self.group:
            if group_results == set(['successful']):
                result = 'successful'
            elif 'successful' in group_results:
                result = 'partial'
            else:
                result = 'failed'
            self._refresh_icon('_', result)

    def start(self):
        self.refresh()
        gobject.timeout_add(TIMEOUT, self.refresh)

    def quit(self, data=None):
        gtk.main_quit()

    def on_left_click(self, status_icon):
        waterfall = urlparse.urljoin(self.url, 'waterfall')
        webbrowser.open(waterfall)

    def on_right_click(self, data, event_button, event_time):
        self.make_menu(event_button, event_time)

    def make_menu(self, event_button, event_time, data=None):
        menu = gtk.Menu()
        quit_app = gtk.MenuItem("Quit")
        menu.append(quit_app)
        quit_app.connect_object("activate", self.quit, "Quit")
        quit_app.show()
        menu.popup(None, None, None, event_button, event_time)

