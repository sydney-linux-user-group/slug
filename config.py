
import sys

# Add our extra modules to sys.path
sys.path.insert(0, 'third_party/aeoid')
sys.path.insert(0, 'third_party.zip/python-dateutil-1.5')
sys.path.insert(0, 'third_party.zip/python-datetime-tz')
sys.path.insert(0, 'third_party.zip/pytz/src')
sys.path.insert(0, 'third_party.zip/icalendar-2.1/src')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

