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

    fixtures = [ 'test_admin_user', 'test_existing_user' ]

    def do_create_event(self, friday=1):
        self.browser.find_element_by_id("add_event").click()
        fridays = Select(self.browser.find_element_by_id("fridays"))
        fridays.select_by_index(friday)
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

    def do_two_events(self):
        self.doLogin()
        #create first event
        event_url = self.do_create_event()
        first_event_id, _ = self.get_id_and_action_from_url(event_url)
        #create second event
        event_url = self.do_create_event(friday=2)
        second_event_id, _ = self.get_id_and_action_from_url(event_url)
        #Go to events page; publish first event
        self.browser.find_element_by_id("events_link").click()
        submit = self.browser.find_element_by_id("submit_%s" % first_event_id)
        submit.click()
        self.doLogout()

        return first_event_id, second_event_id

    def testCreateEvent(self):
        """Create event; should not get a Traceback. Should end up on /edit"""
        self.doLogin()
        event_url = self.do_create_event()
        event_id, event_action = self.get_id_and_action_from_url(event_url)
        self.assertEqual(event_action, 'edit')
        self.assertNotIn(u"Traceback", self.browser.page_source)
        self.assertIn(u"Suggest or sign up", self.browser.page_source)

    def testNewEventReadyToPublish(self):
        """Newly created events should be in the unpublished state."""
        self.doLogin()
        event_url = self.do_create_event()
        event_id, _ = self.get_id_and_action_from_url(event_url)
        self.browser.find_element_by_id("events_link").click()
        submit = self.browser.find_element_by_id("submit_%s" % event_id)
        submit_text = submit.get_attribute("value")
        self.assertEqual(u"Publish event", submit_text, msg=submit)

    def testUnpublishedEventInvisibleToAnonymousUsers(self):
        """Create two events; publish one; log out. Should only see one event."""
        first_event_id, second_event_id = self.do_two_events()
        #Check that the front page rendered okay
        self.assertNotIn(u"Traceback", self.browser.page_source)
        self.assertEqual(self.browser.current_url, self.live_server_url + u"/")
        #Check that we can see the first event
        first_event_item = self.browser.find_element_by_id(
                "event_item_%s" % first_event_id)
        #Check that we can't see the second event
        self.assertNotIn(u"event_item_%s" % second_event_id,
                self.browser.page_source)

    def testUnpublishedEventInvisibleToOrdinaryUsers(self):
        """Create two events; publish one; log out, log in as ordinary user.
           Should only see one event."""
        first_event_id, second_event_id = self.do_two_events()
        #Log in
        self.doLogin(username="existing",password="password")
        #Check that the front page rendered okay
        self.assertNotIn(u"Traceback", self.browser.page_source)
        self.assertEqual(self.browser.current_url, self.live_server_url + u"/")
        #Check that we can see the first event
        first_event_item = self.browser.find_element_by_id(
                "event_item_%s" % first_event_id)
        #Check that we can't see the second event
        self.assertNotIn(u"event_item_%s" % second_event_id,
                self.browser.page_source)
