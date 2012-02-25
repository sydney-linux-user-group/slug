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


class TestLogin(SeleniumTestCase):

    fixtures = [ 'test_admin_user' ]

    def do_login(self):
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        self.browser.switch_to_window("login")
        time.sleep(5) # FIXME(mithro): Change this to a normal for something...
        self.browser.find_element_by_name("username").send_keys("admin")
        self.browser.find_element_by_id("id_password").send_keys("admin")
        self.browser.find_element_by_id("submit_login").click()
        time.sleep(5) # FIXME(mithro): Change this to a normal for something...
        self.browser.switch_to_window(self.main_window_handle)

    def do_create_event(self):
        self.browser.find_element_by_id("add_event").click()
        time.sleep(5) # FIXME(jpolley): Wait for page to load
        fridays = Select(self.browser.find_element_by_id("fridays"))
        fridays.select_by_index(1)
        templates = Select(self.browser.find_element_by_id("templates"))
        templates.select_by_visible_text("slugmeeting")
        self.browser.find_element_by_id("event_name").send_keys("Sample Event")
        self.browser.find_element_by_id("submit_event").click()
        event_url = self.browser.current_url
        return event_url

    def testLoginAndLogout(self):
        self.assertEqual(1, len(self.browser.window_handles))
        self.do_login()
        self.assertEqual(1, len(self.browser.window_handles))
        self.assertIn("Sydney Linux User Group", self.browser.title)
        logout_link = self.browser.find_element_by_id("logout_link")
        logout_link.click()

    def testCreateEvent(self):
        self.do_login()
        event_url = self.do_create_event()
        event_url = event_url.split('/')[-3:]
        event_id = event_url[1]
        self.assertIn(u"Suggest or sign up", self.browser.page_source)




