#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Uses webdriver to test the login work flow.

Steps are:
 * A new user can sign up for the website.
 * Can sign up for an event.
 * Can cancel their sign up.

"""

import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

from django.core import mail
from django.utils import unittest
from django import test as djangotest

from base import SeleniumTestCase


class TestAnonymousUserClicksOffer(SeleniumTestCase):

    def test_anonymous_user_clicks_offer_talk(self):
        self.assertEqual(1, len(self.browser.window_handles))
        offer_link = self.browser.find_element_by_id('offer')
        self.assertEqual(1, len(self.browser.window_handles))

class TestLoggedInUserClicksOffer(SeleniumTestCase):

    fixtures = [ 'test_admin_user', 'test_existing_user' ]

    def test_logged_in_user_clicks_offer_talk(self):
        """Check that talk offer page opens in new window"""
        self.doLogin(username="existing", password="password")
        self.assertEqual(1, len(self.browser.window_handles))
        offer_link = self.browser.find_element_by_id('offer')
        self.assertEqual(1, len(self.browser.window_handles))
