#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""
"""

from django.utils import unittest
from django import test as djangotest


class FixFixturesTestCase(unittest.TestCase):

    def testNonExistant(self):
        suite = unittest.TestSuite()

        class TestTestCase(djangotest.TransactionTestCase):
            fixtures = ['nonexistent']

        testPass = False
        try:
            suite.addTest(TestTestCase())
        except AssertionError, e:
            testPass = True

        self.assertTrue(testPase)
