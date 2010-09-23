import os
import sys
import gtk
import optparse
from ConfigParser import ConfigParser

from bbnotify.notificator import Notificator
from bbnotify.daemonize import daemonize



def main():
    usage = """Usage: %prog [options] http://buildboturl/xmlrpc"""
    url = None
    ignore_builders = None

    # parse ~/.bbnotifyrc
    cp = ConfigParser({'url': "", 'ignore-builders': ""})
    configfile = os.path.expanduser("~/.bbnotifyrc")
    if os.path.exists(configfile):
        cp.read(configfile)
        url = cp.get("bbnotify", "url")
        ignore_builders = cp.get("bbnotify", "ignore-builders").split()

    # parse commandline options
    parser = optparse.OptionParser()
    parser.add_option("-f", "--forward", dest="nodaemon",
        action="store_true", default=False,
        help="don't run in background")
    parser.add_option("-i", "--ignore-builder", dest="ignore_builders",
        metavar="builder_name", action="append", default=None,
        help="don't display the status of this builder")
    parser.set_usage("%s\n%s" % (usage, parser.format_option_help()))
    (options, args) = parser.parse_args()
    if options.ignore_builders is not None:
        ignore_builders = options.ignore_builders
    if len(args) > 0:
        url = args[0]
    if not url:
        parser.error("Missing url")

    # run!
    Notificator(url, ignore_builders)
    if not options.nodaemon:
        daemonize()
    gtk.main()
