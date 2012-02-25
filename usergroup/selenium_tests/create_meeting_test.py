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


class TestEventCreationAndPublication(SeleniumTestCase):

    fixtures = [ 'test_admin_user' ]

    def do_create_event(self):
        self.browser.find_element_by_id("add_event").click()
        fridays = Select(self.browser.find_element_by_id("fridays"))
        fridays.select_by_index(1)
        templates = Select(self.browser.find_element_by_id("templates"))
        templates.select_by_visible_text("slugmeeting")
        self.browser.find_element_by_id("event_name").send_keys("Sample Event")
        self.browser.find_element_by_id("submit_event").click()
        event_url = self.browser.current_url
        return event_url

    def get_id_and_action_from_url(self, event_url):
        event_url = event_url.split('/')[-3:]
        event_id = event_url[1]
        event_action = event_url[2]
        return event_id, event_action

    def testLoginAndLogout(self):
        self.assertEqual(1, len(self.browser.window_handles))
        self.doLogin()
        self.assertEqual(1, len(self.browser.window_handles))
        self.assertIn("Sydney Linux User Group", self.browser.title)
        logout_link = self.browser.find_element_by_id("logout_link")
        logout_link.click()

    def testCreateEvent(self):
        self.doLogin()
        event_url = self.do_create_event()
        event_id, event_action = self.get_id_and_action_from_url(event_url)
        self.assertEqual(event_action, 'edit')
        self.assertNotIn(u"Traceback", self.browser.page_source)
        self.assertIn(u"Suggest or sign up", self.browser.page_source)

    def testNewEventReadyToPublish(self):
        self.doLogin()
        event_url = self.do_create_event()
        event_id, _ = self.get_id_and_action_from_url(event_url)
        self.browser.find_element_by_id("events_link").click()
        submit = self.browser.find_element_by_id("submit_%s" % event_id)
        submit_text = submit.get_attribute("value")
        self.assertEqual(u"Publish event", submit_text, msg=submit)

    def testUnpublishedEventInvisibleToAnonymousUsers(self):
        self.doLogin()
        event_url = self.do_create_event()
        event_url = event_url.split('/')[-3:]
        event_id = event_url[1]
        self.doLogout()
        self.browser.get("%s" % self.live_server_url)
