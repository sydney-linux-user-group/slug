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


class TestRegister(SeleniumTestCase):
    fixtures = ['test_existing_user']

    def doOpenLogin(self):
        self.assertEqual(1, len(self.browser.window_handles))
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        WebDriverWait(self.browser, 30).until(lambda b: len(b.window_handles) > 1)
        self.browser.switch_to_window("login")
        self.browser.find_elements_by_name("username")

    def testFailOnMissingField(self):
        self.doOpenLogin()
        self.browser.find_elements_by_name("username")[-1].send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())
        self.assertIn(
            "field is required",
            self.browser.find_element_by_class_name("errorlist").text.lower()
            )

    def testFailOnNonMatchingPasswords(self):
        self.doOpenLogin()
        self.browser.find_elements_by_name("username")[-1].send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("testing@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword2")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())
        self.assertIn(
            "didn't match",
            self.browser.find_element_by_class_name("errorlist").text.lower()
            )

    def testFailOnInvalidEmailAddress(self):
        self.doOpenLogin()
        self.browser.find_elements_by_name("username")[-1].send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("testing.example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())
        self.assertIn(
            "valid e-mail address",
            self.browser.find_element_by_class_name("errorlist").text.lower()
            )

    def testFailOnExistingUsername(self):
        self.doOpenLogin()
        self.browser.find_elements_by_name("username")[-1].send_keys("existing")
        self.browser.find_element_by_id("id_email").send_keys("testing@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())
        self.assertIn(
            "username already exists",
            self.browser.find_element_by_class_name("errorlist").text.lower()
            )

    def testFailOnExistingEmail(self):
        self.doOpenLogin()
        self.browser.find_elements_by_name("username")[-1].send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("existing@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())
        self.assertIn(
            "already in use",
            self.browser.find_element_by_class_name("errorlist").text.lower()
            )

    def testRegistrationSuccess(self):
        self.doOpenLogin()
        self.browser.find_elements_by_name("username")[-1].send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("test@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        WebDriverWait(self.browser, 30).until(lambda b: len(b.window_handles) == 1)
        self.browser.switch_to_window(self.main_window_handle)
        self.assertIn("Sydney Linux User Group", self.browser.title)

        # Logout
        self.doLogout()

        # Try and login again
        self.doLogin("test", "testingpassword1")
        self.doLogout()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, "Please confirm your email address")

        activate_groups = re.search(r"(/accounts/activate/[0-9a-f]+/)", str(mail.outbox[0].body))
        activate_link = activate_groups.groups()[0]

        self.browser.get("%s%s" % (self.live_server_url, activate_link))
        self.doLogout()
