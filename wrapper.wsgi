""" WSGI wrapper for ask """

import os, sys
path = os.path.dirname(__file__)
if path not in sys.path:
	sys.path.insert(0, path)

lib_path = os.path.join( path, 'lib/Lib/site-packages' )
if lib_path not in sys.path:
	sys.path.insert( 0, lib_path )

app_path = os.path.join( path, 'apps' )
if app_path not in sys.path:
	sys.path.insert( 0, app_path )






from ask import application