#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""
Fix the fixture loading so that it errors if a fixture is not found.
"""

import cStringIO as StringIO
import sys

from django.core.management import call_command
from django import test as djangotest
from django.db import connections, DEFAULT_DB_ALIAS


def _load_fixture(db, fixture, _sys_stdout=sys.stdout):
    print "Loading fixture", fixture
    sys.stdout = StringIO.StringIO()
    call_command('loaddata', *[fixture], **{
        'verbosity': 1,
        'commit': False,
        'database': db
        })
    cmd_stdout, sys.stdout = sys.stdout, _sys_stdout
    assert "No fixtures found." not in cmd_stdout.getvalue(), \
        "Was not able to find fixture %s" % fixture
    print cmd_stdout.getvalue()
    sys.stdout = _sys_stdout


def _TransactionTestCase_fixture_setup(self, _real_fixture_setup=djangotest.TransactionTestCase._fixture_setup):
    if getattr(self, 'multi_db', False):
        databases = connections
    else:
        databases = [DEFAULT_DB_ALIAS]

    for db in databases:
        call_command('flush', verbosity=0, interactive=False, database=db)
        if not hasattr(self, 'fixtures'):
            continue

        for fixture in self.fixtures:
            _load_fixture(db, fixture)

djangotest.TransactionTestCase._fixture_setup = _TransactionTestCase_fixture_setup


def _TestCase_fixture_setup(self, _real_fixture_setup=djangotest.TestCase._fixture_setup):
    # Call the original fixture setup
    _real_fixture_setup(self)

    if getattr(self, 'multi_db', False):
        databases = connections
    else:
        databases = [DEFAULT_DB_ALIAS]

    for db in databases:
        if not hasattr(self, 'fixtures'):
            continue

        for fixture in self.fixtures:
            _load_fixture(db, fixture)

djangotest.TestCase._fixture_setup = _TestCase_fixture_setup
