#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://localhost:8000")
assert "Sydney Linux User Group" in browser.title
login_link = browser.find_element_by_xpath
login_link = browser.find_element_by_class_name("openid_login")
login_link.click()

browser.switch_to_window("login")
browser.find_element_by_id("id_username").send_keys("admin")
browser.find_element_by_id("id_password").send_keys("password")
browser.find_element_by_id("submit_login").click()

browser.switch_to_window("parent")
browser.close()
