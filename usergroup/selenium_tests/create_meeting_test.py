#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from selenium import webdriver
from selenium.selenium import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

from django.utils import unittest
from django import test as djangotest

from base import SeleniumTestCase


class TestLogin(SeleniumTestCase):

    fixtures = [ 'test_admin_user' ]

    def testLoginAndLogout(self):
        self.assertEqual(1, len(self.browser.window_handles))
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        self.browser.switch_to_window("login")
        time.sleep(5) # FIXME: Change this to a normal for something...
        self.browser.find_element_by_name("username").send_keys("admin")
        self.browser.find_element_by_id("id_password").send_keys("admin")
        self.browser.find_element_by_id("submit_login").click()
        time.sleep(5) # FIXME: Change this to a normal for something...
        self.browser.switch_to_window(self.main_window_handle)
        self.assertEqual(1, len(self.browser.window_handles))
        self.assertIn("Sydney Linux User Group", self.browser.title)
        logout_link = self.browser.find_element_by_id("logout_link")
        logout_link.click()
