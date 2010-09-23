import sys
import os.path
import gtk
import optparse
from ConfigParser import ConfigParser

from bbnotify.notificator import Notificator
from bbnotify.daemonize import daemonize


def main():
    usage = "usage: %prog [options] http://buildboturl/xmlrpc"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-f", "--forward", dest="nodaemon",
        action="store_true", default=False,
        help="don't run in background")
    parser.add_option("-i", "--ignore-builder", dest="ignore_builders",
        metavar="builder_name", action="append", default=[],
        help="don't display the status of this builder")

    (options, args) = parser.parse_args()

    url=None

    """
    We try to read a configurationfile ~/.bbnotifyrc of the following form
[bbnotify]
url=http://buildboturl/xmlrpc
ignore_builders=list of builders to ignore

    Options from the commandline takes precedence over the configuration file
    """
    configfile=os.path.expanduser("~/.bbnotifyrc")
    if os.path.exists(configfile):
        cp = ConfigParser()
        cp.read(configfile)
        if cp.has_option("bbnotify", "url"):
            url = cp.get("bbnotify", "url")
        if options.ignore_builders is None and cp.has_option("bbnotify", "ignore_builders"):
            options.ignore_builders = cp.get("bbnotify", "ignore_builders").split()

    if len(args) > 0:
        url=args[0]

    if url is None:
        parser.error("missing url")

    Notificator(url, options.ignore_builders)
    if not options.nodaemon:
        daemonize()
    gtk.main()
