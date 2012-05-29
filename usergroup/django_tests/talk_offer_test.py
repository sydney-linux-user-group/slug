#!/usr/bin/env python
"""Tests around creating, publishing, and announcing meetings.

Does not use selenium, so cannot test client behaviour."""

import datetime
import random

import django.test

import usergroup.event_edit

#TestCases have lots of public methods
#pylint: disable=R0904

class TestTalkOfferLogin(django.test.TestCase):
    """Before we test anything else, let's see if login actually works"""
    fixtures = ['test_admin_user', 'test_existing_user']

    def test_offer_page(self):
        """Ensure that the offer page loads."""
        self.client.login(username='existing', password='password')
        offer_page = self.client.get("/offer/add")
        self.assertContains(offer_page, 'input name="consent"')


