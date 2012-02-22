#!/usr/bin/env python

from selenium import webdriver
from selenium.selenium import selenium
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
        self.assertIn("Sydney Linux User Group", self.browser.title)

    def tearDown(self):
        LiveServerTestCase.tearDown(self)
        self.browser.quit()

class TestLogin(LiveServerTestCase):

    fixtures = [ 'test_admin_user' ];

    def setUp(self):
        self.browser = webdriver.Firefox() # Get local session of firefox
        self.browser.get("%s" % self.live_server_url)

    def testLogin(self):
        self.assertEqual(1, len(self.browser.window_handles))
        main_window_handle = self.browser.window_handles[0]
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        self.browser.switch_to_window("login")
        self.browser.find_element_by_name("username").send_keys("admin")
        self.browser.find_element_by_id("id_password").send_keys("admin")
        self.browser.find_element_by_id("submit_login").click()
        time.sleep(30)
        self.browser.switch_to_window(main_window_handle)
        self.assertEqual(1, len(self.browser.window_handles))
        self.assertIn("Sydney Linux User Group", self.browser.title)
        logout_link = self.browser.find_element_by_id("logout_link")
        logout_link.click()


    def tearDown(self):
        #LiveServerTestCase.tearDown(self)
        #self.browser.quit()
        pass
