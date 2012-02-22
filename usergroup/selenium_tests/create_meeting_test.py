#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

from django.utils import unittest
from django import test as djangotest

from liveserver.test.testcases import LiveServerTestCase

class SeleniumBasicsTestCase(LiveServerTestCase):

    def testBasics(self):
        self.browser = webdriver.Firefox() # Get local session of firefox
        self.browser.get("%s" % self.live_server_url)
        self.assertIn("Sydney Linux User Group", browser.title)

    def tearDown(self):
        LiveServerTestCase.tearDown(self)
        self.browser.quit()

class TestLogin(LiveServerTestCase):

    fixtures = [ 'test_admin_user' ];

    def setUp(self):
        self.browser = webdriver.Firefox() # Get local session of firefox
        self.browser.get("%s" % self.live_server_url)

    def testLogin(self):
        login_link = self.browser.find_element_by_xpath
        login_link = self.browser.find_element_by_class_name("openid_login")
        login_link.click()
        self.browser.switch_to_window("login")
        self.browser.find_element_by_id("id_username").send_keys("admin")
        self.browser.find_element_by_id("id_password").send_keys("password")
        self.browser.find_element_by_id("submit_login").click()
        self.browser.switch_to_window("parent")

    def tearDown(self):
        LiveServerTestCase.tearDown(self)
        self.browser.quit()
