#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from selenium import webdriver
from selenium.selenium import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

from django.utils import unittest
from django import test as djangotest

from base import SeleniumTestCase

class TestValidAdminLogin(SeleniumTestCase):

    fixtures = [ 'test_admin_user' ]

    def testLoginAndLogout(self):
        self.assertEqual(1, len(self.browser.window_handles))
        self.doLogin()
        self.assertEqual(1, len(self.browser.window_handles))
        self.assertIn("Sydney Linux User Group", self.browser.title)

class TestInvalidUserLogin(SeleniumTestCase):

    fixtures = [ 'test_admin_user' ]

    def testInvalidLogin(self):
        self.doLogin(username="notexisting", password="wrong", wait=False)
        #Login window should still be active
        self.assertEqual(2, len(self.browser.window_handles))
        #No traceback thanks
        self.assertNotIn(u"Traceback", self.browser.page_source)
        #Should have an error message
        self.assertIn(u"Please enter a correct username and password.",
                self.browser.page_source)

class TestValidNonAdminLogin(SeleniumTestCase):

    fixtures = [ 'test_admin_user', 'test_existing_user' ]

    def testLoginAndLogout(self):
        self.assertEqual(1, len(self.browser.window_handles))
        self.doLogin(username="existing", password="password")
        self.assertEqual(1, len(self.browser.window_handles))
        self.assertIn("Sydney Linux User Group", self.browser.title)
