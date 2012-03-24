#!/usr/bin/python
"""Tests around creating and manipulating meetings"""
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from selenium.webdriver.support.ui import Select

from .base import SeleniumTestCase

class TestEventCreationAndPublication(SeleniumTestCase):
    """Tests of event creation and publishing."""

    fixtures = [ 'test_admin_user', 'test_existing_user' ]

    def do_create_event(self, friday=1):
        """Common routine - create an event."""
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
        """Split ``event_url`` into event_id and event_action."""
        event_url = event_url.split('/')[-3:]
        event_id = event_url[1]
        event_action = event_url[2]
        return event_id, event_action

    def testUnpublishedEventInvisibleToAnonymousUsers(self):
        """Create two events; publish one; log out. Should only see one."""
        #FIXME: Nothing being tested here is clientside, so use the test client
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
        #FIXME: Nothing being tested here is clientside, so use the test client
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
