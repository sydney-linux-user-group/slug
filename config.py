
import sys

def sys_path_insert(module):
	if module not in sys.path:
		sys.path.insert(0, module)

def setup():
	# Add our extra modules to sys.path
	sys_path_insert('third_party/aeoid')
	sys_path_insert('third_party.zip/python-dateutil-1.5')
	sys_path_insert('third_party.zip/python-datetime-tz')
	sys_path_insert('third_party.zip/pytz/src')
	sys_path_insert('third_party.zip/icalendar-2.1/src')

	import os
	os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	from google.appengine.dist import use_library
	use_library('django', '1.2')
