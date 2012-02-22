#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import os
import re
import subprocess

from django.conf import settings
from django.db.models import get_app
from django.utils import unittest
from django.test import simple as testsuite
from django.test import testcases


class RealDisplay(object):
    """Use the users display."""

    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class VNCDisplay(object):
    """Use a VNCServer for display."""

    def __init__(self, viewer=False):
        self.display = ':10'
        self.original = os.getenv('DISPLAY')

        self.vncserver = None

        self.viewer = viewer

    def __enter__(self):
        # Start the VNCServer
        p = subprocess.Popen(
            ' '.join(['vncserver', self.display, '-SecurityTypes', 'None']),
            shell=True,
            stdout=file('vncserver.stdout', 'w'),
            stderr=subprocess.STDOUT,
            )
        p.wait()
        self.vncserver = 'RUNNING'

        # Set the environment
        os.environ['DISPLAY'] = ':10'

        # Start a window manager
        winman = subprocess.Popen(
            ' '.join(['ratpoison']),
            shell=True,
            )

        # Start a viewer if needed
        if self.viewer:
            viewer = subprocess.Popen(
                ' '.join(['vncviewer', self.display]),
                shell=True,
                stdout=file('vncviewer.stdout', 'w'),
                stderr=subprocess.STDOUT,
                env={'DISPLAY': self.original},
                )

    def __exit__(self, exc_type, exc_value, traceback):
        if self.vncserver == 'RUNNING':
            os.putenv('DISPLAY', self.original)

            p = subprocess.Popen(
                ' '.join(['vncserver', '-kill', self.display]),
                shell=True,
                )
            p.wait()

            self.vncserver = 'TERMINATED'


import cStringIO as StringIO
import sys
from django import test as djangotest
from django.db import connections, DEFAULT_DB_ALIAS
from django.core.management import call_command

def _fixture_setup(self, _real_fixture_setup=djangotest.TestCase._fixture_setup, _sys_stdout=sys.stdout):
    _real_fixture_setup(self)

    if getattr(self, 'multi_db', False):
        databases = connections
    else:
        databases = [DEFAULT_DB_ALIAS]

    for db in databases:
        if hasattr(self, 'fixtures'):
            for fixture in self.fixtures:
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

djangotest.TestCase._fixture_setup = _fixture_setup

class UserGroupTestSuiteRunner(testsuite.DjangoTestSuiteRunner):
    """A test suite runner which can use a display."""

    def setup_test_environment(self, **kwargs):
        testsuite.setup_test_environment()
        settings.DEBUG=False
        unittest.installHandler()

    def filter_suite(self, suite, pred):
        """Recursively filter test cases in a suite based on a predicate."""
        newtests = []
        for test in suite._tests:
            if test.__class__.__name__.endswith('TestSuite'):
                self.filter_suite(test, pred)
                newtests.append(test)
            else:
                if pred(test):
                    newtests.append(test)
        suite._tests = newtests

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = unittest.TestSuite()

        if test_labels:
            for label in test_labels:
                appname, test = label.split('.', 1)

                def filter_test(testcase, testprefix=label):
                    testname = "%s.%s" % (testcase.__class__.__module__, testcase.__class__.__name__)
                    return testname.startswith(testprefix)

                app = get_app(appname)
                suite.addTest(testsuite.build_suite(app))
                self.filter_suite(suite, filter_test)
        else:
            for appname in settings.OUR_APPS:
                app = get_app(appname, emptyOK=True)
                if app is None:
                    continue
                suite.addTest(testsuite.build_suite(app))

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return testsuite.reorder_suite(suite, (testcases.TestCase,))

    def run_tests(self, *args, **kwargs):
        if os.environ.get('TEST_DISPLAY', '') in ('1', 'True'):
            server = RealDisplay()
        else:
            server = VNCDisplay()

        with server:
            return testsuite.DjangoTestSuiteRunner.run_tests(self, *args, **kwargs)


def suite():
    mylocation = os.path.dirname(__file__)

    suite = unittest.TestSuite()
    for dirpath, dirnames, filenames in os.walk(mylocation):
        for filename in filenames:
            remaining = dirpath[len(os.path.commonprefix([mylocation, dirpath])):].replace('/', '.')
            test = "usergroup%s.%s" % (remaining, filename[:-3])

            # Unittest test
            if filename.endswith('_test.py'):
                suite.addTest(unittest.TestLoader().loadTestsFromName(test))

    return suite
