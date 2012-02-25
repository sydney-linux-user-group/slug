#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import cStringIO as StringIO

import os
import re
import subprocess
import sys

from django import test as djangotest
from django.core.management import call_command
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.models import get_app
from django.utils import unittest
from django.test import simple as testsuite
from django.test import testcases

from usergroup.test_utils import fix_fixtures
from usergroup.test_utils import fix_exceptions
from usergroup.test_utils import display_servers


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
                    testname = "%s.%s.%s" % (testcase.__class__.__module__, testcase.__class__.__name__, testcase)
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
            server = display_servers.RealDisplay()
        else:
            server = display_servers.VNCDisplay()

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
