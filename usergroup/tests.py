#!/usr/bin/env python

from django.utils import unittest
import os
import re

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
