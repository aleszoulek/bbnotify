BBNotify
========

Description
-----------

Monitors activity of buildbot server.
  1. Displays status icon in tray icon
  2. Notifies on new build completed

Install
-------

::

 pip install -e 'git://github.com/aleszoulek/bbnotify.git#egg=bbnotify'

Usage
-----

::

 Usage: bbnotify.py [options] http://buildboturl/xmlrpc
 
 Options:
   -h, --help            show this help message and exit
   -f, --forward         don't run in background
   -i builder_name, --ignore-builder=builder_name
                         don't display the status of this builder
  -I builder_name, --include-builder=builder_name
                        include only listed builders
  -p [xmlrpc|json], --protocol=[xmlrpc|json] (default xmlrpc)
                        protocol to use when comunicating with buildbot



Using a configuration file
--------------------------
You can save some of your options in the file ~/.bbnotifyrc in the form

::

 [bbnotify]
 url=http://buildboturl/xmlrpc
 ignore-builders=list of builders to ignore
 include-builders=list of builders to include
 protocol=json|xmlrpc


