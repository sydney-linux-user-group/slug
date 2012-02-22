#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import unittest2 as unittest

class TestBasicSeleniumality(unittest.TestCase):

    def testBasics(self):
        browser = webdriver.Firefox() # Get local session of firefox
        browser.get("http://localhost:8000")
        self.assertIn("Sydney Linux User Group", browser.title)

    def tearDown(self):
        self.browser.close()

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox() # Get local session of firefox
        self.browser.get("http://localhost:8000")

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
        self.browser.close()
