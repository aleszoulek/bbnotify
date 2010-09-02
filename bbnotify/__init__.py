import sys
import gtk

from bbnotify.notificator import Notificator
from bbnotify.daemonize import daemonize


def main():
    if len(sys.argv) == 1:
        sys.stderr.write('Usage: bbnotify.py [ENDPOINT]\n')
        sys.exit(1)
    Notificator(sys.argv[1])
    daemonize()
    gtk.main()

