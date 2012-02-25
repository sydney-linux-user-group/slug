#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import time

from selenium import webdriver
from selenium.selenium import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from django.conf import settings
from django.utils import unittest
import django.test

from liveserver.test.testcases import LiveServerTestCase


class BrowserQuitter(object):
    """Helper class which always causes the browser object to close."""
    def __init__(self, browser):
        self.browser = browser

    def __del__(self):
        self.browser.close()
        self.browser.quit()


class SeleniumTestCase(LiveServerTestCase):
    fixtures = []

    def setUp(self):
        LiveServerTestCase.setUp(self)

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.browser_quiter = BrowserQuitter(self.browser)

        self.browser.get("%s" % self.live_server_url)
        self.assertIn("Sydney Linux User Group", self.browser.title)
        self.main_window_handle = self.browser.window_handles[0]

    def tearDown(self):
        del self.browser_quiter
        LiveServerTestCase.tearDown(self)

    def doLogin(self, username, password):
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        self.browser.switch_to_window("login")
        self.browser.find_element_by_name("username").send_keys("admin")
        self.browser.find_element_by_id("id_password").send_keys("admin")
        self.browser.find_element_by_id("submit_login").click()
        self.browser.switch_to_window(self.main_window_handle)
        self.assertIn("Sydney Linux User Group", self.browser.title)

    def doLogout(self):
        self.browser.switch_to_window(self.main_window_handle)
        logout_link = self.browser.find_element_by_id("logout_link")
        logout_link.click()

