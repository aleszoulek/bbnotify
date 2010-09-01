import sys
import gtk

from bbnotify.notificator import Notificator



def main():
    Notificator(sys.argv[1])
    gtk.main()

