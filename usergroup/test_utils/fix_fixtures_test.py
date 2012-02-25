#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""
"""

from django.utils import unittest
from django import test as djangotest

from usergroup.test_utils import fix_fixtures


class FixFixturesTestCase(unittest.TestCase):

    def testNonExistant(self):
        class TestTestCase(djangotest.TransactionTestCase):
            fixtures = ['nonexistent']

            def testNop(self):
                print "testNop 1"
                self.asserTrue(True)
                print "testNop 2"

        r = unittest.TestResult()
        TestTestCase('testNop')(r)
        self.assertEqual(r.errors[0][-1].split('\n')[-2], "AssertionError: Was not able to find fixture nonexistent")
