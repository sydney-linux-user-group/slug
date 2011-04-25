#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module which setups our configuration environment.

**
Everything code should import this module and run the setup function before
doing anything else, *including imports*!
**
"""

import sys


paths = [
    'third_party/aeoid',
    'third_party.zip/python-dateutil-1.5',
    'third_party.zip/python-datetime-tz',
    'third_party.zip/icalendar-2.1/src',
    'third_party.zip/vobject'
    'third_party.zip/Markdown-2.0.3',
]


def sys_path_insert(ipath):
    """Insert a path into sys if it doesn't exist already."""
    if ipath not in sys.path:
        sys.path.insert(0, ipath)


def setup_django():
    """Setup the django settings."""
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from google.appengine.dist import use_library
    use_library('django', '1.2')


def setup():
    """Setup our configuration environment."""

    # Add our extra modules to sys.path
    for ipath in paths:
        sys_path_insert(ipath)

    setup_django()


def lint_setup():
    """Setup called to make pylint work."""
    sys_path_insert('../google_appengine')
    for ipath in paths:
        sys_path_insert(ipath.replace('.zip', ''))

    setup_django()
