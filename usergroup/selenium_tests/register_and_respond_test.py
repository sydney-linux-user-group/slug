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

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

from django.core import mail
from django.utils import unittest
from django import test as djangotest

from base import SeleniumTestCase


class TestRegister(SeleniumTestCase):
    fixtures = ['test_existing_user']

    def testFailOnNonMatchingPasswords(self):
        self.browser.find_element_by_name("username").send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("testing@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword2")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())

    def disabled_testFailOnInvalidEmailAddress(self):
        self.browser.find_element_by_name("username").send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("testing.example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())

    def disabled_testFailOnExistingUsername(self):
        self.browser.find_element_by_name("id_username").send_keys("exist")
        self.browser.find_element_by_id("id_email").send_keys("testing@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())

    def disabled_testFailOnExistingEmail(self):
        self.browser.find_element_by_id("id_username").send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("existing@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())

    def disabled_testRegistrationSuccess(self):
        self.browser.find_element_by_id("id_username").send_keys("test")
        self.browser.find_element_by_id("id_email").send_keys("test@example.com")
        self.browser.find_element_by_id("id_password1").send_keys("testingpassword1")
        self.browser.find_element_by_id("id_password2").send_keys("testingpassword1")
        self.browser.find_element_by_id("submit_create").click()

        self.assertIn("register", self.browser.title.lower())
