#!/usr/bin/env python

import os
import gtk
import gobject
import webbrowser
import urlparse

from os.path import join, dirname, abspath
from datetime import datetime

from bbnotify.connectors import XmlRpc


MEDIA_DIR = join(abspath(dirname(__file__)), 'media')
TIMEOUT = 1000 * 30 # 30 sec



class Notificator(object):
    ICONS = {
        'success': 'green.png',
        'failure': 'red.png',
        'nobuild': 'grey.png',
        'retry': 'grey.png',
        'exception': 'red.png',
    }

    def __init__(self, url, ignore_builders, include_builders):
        if url.endswith('/'):
            url = url[:-1]
        self.url = url
        self.buildbot = XmlRpc(self.url)
        self.url = url
        self.ignore_builders = ignore_builders
        self.include_builders = include_builders
        self.icons = {}
        self.statuses = {}
        self.start()

    def refresh(self):
        for name, status in self.buildbot.get_status().items():
            if name not in self.ignore_builders:
                if self.include_builders and name not in self.include_builders:
                    continue
                if name not in self.icons:
                    self.icons[name] = gtk.StatusIcon()
                    self.icons[name].connect("activate", self.on_left_click)
                    self.icons[name].connect("popup-menu", self.on_right_click)
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

