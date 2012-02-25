#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import cStringIO as StringIO
import os
import sys
import time
import warnings

from selenium import webdriver
from selenium.selenium import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait

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

        profile = FirefoxProfile()
        profile.set_preference('plugins.hide_infobar_for_missing_plugin', True)

        firefox_bin = os.path.join('firefox', 'firefox')
        if os.path.exists(firefox_bin):
            self.browser = webdriver.Firefox(firefox_profile=profile, firefox_binary=FirefoxBinary(firefox_bin))
        else:
            warnings.warn("Using your default firefox, this can be unreliable!")
            self.browser = webdriver.Firefox(firefox_profile=profile)

        self.browser_quiter = BrowserQuitter(self.browser)

        self.browser.implicitly_wait(10)

        self.browser.get("%s" % self.live_server_url)
        self.assertIn("Sydney Linux User Group", self.browser.title)
        self.main_window_handle = self.browser.window_handles[0]

    def _formatMessage(self, msg, standardMsg):
        s = StringIO.StringIO()
        s.write(LiveServerTestCase._formatMessage(self, msg, standardMsg))
        s.write("\n")
        s.write("\n")
        s.write("failure url: %s\n" % self.browser.current_url)
        s.write("failure page source\n")
        s.write("-"*80)
        s.write("\n")
        s.write(self.browser.page_source)
        s.write("\n")
        s.write("-"*80)
        s.write("\n")
        return s.getvalue()

    def tearDown(self):
        del self.browser_quiter
        LiveServerTestCase.tearDown(self)

    def doLogin(self, username, password):
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        self.browser.switch_to_window("login")
        self.browser.find_elements_by_name("username")[0].send_keys(username)
        self.browser.find_element_by_id("id_password").send_keys(password)
        self.browser.find_element_by_id("submit_login").click()

        WebDriverWait(self.browser, 30).until(lambda b: len(b.window_handles) == 1)
        self.browser.switch_to_window(self.main_window_handle)
        self.assertIn("Sydney Linux User Group", self.browser.title)

    def doLogout(self):
        self.browser.switch_to_window(self.main_window_handle)
        logout_link = self.browser.find_element_by_id("logout_link")
        logout_link.click()

