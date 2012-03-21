#!/usr/bin/env python
"""Tests around creating, publishing, and announcing meetings.

Does not use selenium, so cannot test client behaviour."""

import datetime
import random

import django.test

import usergroup.event_edit

#TestCases have lots of public methods
#pylint: disable=R0904

class TestLogin(django.test.TestCase):
    """Before we test anything else, let's see if login actually works"""
    fixtures = ['test_admin_user', 'test_existing_user']

    def test_admin_login(self):
        "Verify that admins can log in."""
        login_status = self.client.login(username='admin', password='admin')
        self.assertTrue(login_status)

    def test_nonadmin_login(self):
        """Verify that non-admins can log in."""
        login_status = self.client.login(username='existing',
                                         password='password')
        self.assertTrue(login_status)

