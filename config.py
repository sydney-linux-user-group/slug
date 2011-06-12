#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module which setups our configuration environment.

**
Everything should import this module and run the setup function before
doing anything else, *including imports*!
**
"""

import sys
import os

HOST = None

def getpaths():
    """Get the extra third_party paths we need."""
    paths = set()
    for line in file('third_party.paths', 'r'):
        if line.startswith('#'):
            continue
        paths.add(line.strip().split(' ', 1)[0])

    paths = list(paths)
    paths.sort()
    return paths


def sys_path_insert(ipath):
    """Insert a path into sys if it doesn't exist already."""
    if ipath not in sys.path:
        sys.path.insert(0, ipath)


def setup_django():
    """Setup the django settings."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from google.appengine.dist import use_library
    use_library('django', '1.2')


def setup(host=None):
    """Setup our configuration environment."""
    global HOST # pylint: disable-msg=W0603
    if HOST is None:
        if host is None:
            HOST = 'signup.slug.org.au'
        else:
            HOST = host

    # Add our extra modules to sys.path
    sys_path_insert('third_party.zip')
    for ipath in getpaths():
        if 'third_party.zip' in ipath:
            continue
        sys_path_insert(ipath)

    setup_django()


def lint_setup():
    """Setup called to make pylint work."""
    if not "APPENGINE_SDK" in os.environ:
        print "Please set $APPENGINE_SDK to the location of the appengine SDK."
        return 1

    print "APPENGINE_SDK at ", os.environ["APPENGINE_SDK"]
    sys_path_insert(os.environ["APPENGINE_SDK"])

    for ipath in getpaths():
        sys_path_insert(ipath.replace('.zip', ''))

    setup_django()

if __name__ == "__main__":
    for path in getpaths():
        print path
