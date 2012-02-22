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

browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://localhost:8000")

login_link = browser.find_elements_by_class_name("openid_login")
login_link[0].click()

browser.switch_to_window("login")

# Check that non-matching passwords fail
browser.find_element_by_name("username").send_keys("test")
browser.find_element_by_id("id_email").send_keys("testing@example.com")
browser.find_element_by_id("id_password1").send_keys("testingpassword1")
browser.find_element_by_id("id_password2").send_keys("testingpassword2")
browser.find_element_by_id("submit_create").click()

# Check that email address fail
browser.find_element_by_name("username").send_keys("test")
browser.find_element_by_id("id_email").send_keys("testing.example.com")
browser.find_element_by_id("id_password1").send_keys("testingpassword1")
browser.find_element_by_id("id_password2").send_keys("testingpassword1")
browser.find_element_by_id("submit_create").click()

# Check that an existing user fails
browser.find_element_by_name("id_username").send_keys("exist")
browser.find_element_by_id("id_email").send_keys("testing@example.com")
browser.find_element_by_id("id_password1").send_keys("testingpassword1")
browser.find_element_by_id("id_password2").send_keys("testingpassword1")
browser.find_element_by_id("submit_create").click()

# Check that an existing user fails
browser.find_element_by_id("id_username").send_keys("test")
browser.find_element_by_id("id_email").send_keys("existing@example.com")
browser.find_element_by_id("id_password1").send_keys("testingpassword1")
browser.find_element_by_id("id_password2").send_keys("testingpassword1")
browser.find_element_by_id("submit_create").click()

# Check that everything good works
browser.find_element_by_id("id_username").send_keys("test")
browser.find_element_by_id("id_email").send_keys("test@example.com")
browser.find_element_by_id("id_password1").send_keys("testingpassword1")
browser.find_element_by_id("id_password2").send_keys("testingpassword1")
browser.find_element_by_id("submit_create").click()



