#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

import logging

# AppEngine Imports
from google.appengine.ext import webapp

# Third Party imports

# Our App imports
import models
from utils.render import render as r


class EditOffer(webapp.RequestHandler):
    """Handler for creating and editing Offer objects."""

    def get(self, key=None):
        user = users.get_current_user()
        if not user:
          self.redirect(users.create_login_url(self.request.url))
          return
        if key:
            try:
                key = long(key)
                offer = models.TalkOffer.get_by_id(key)
                assert offer
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/events')
                return
        else:
            offer = None

        self.response.out.write(r(
            'templates/offertalk.html', locals()
            ))

    def post(self, key=None):
        user = users.get_current_user()
        if not user:
          self.redirect(users.create_login_url(self.request.url))
          return

        if key:
            try:
                key = long(key)
                offer = models.TalkOffer.get_by_id(key)
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/offers')
                return
        else:
            u_key = user.user_id()
            offer = models.TalkOffer(name=self.request.get('name'), parent=u_key)

        user_time = self.request.get('minutes')
        if 's' in user_time:
            user_time.replace('s', '')
            seconds = int(user_time)
        else:
            user_time.replace('m', '')
            seconds = 60 * int(user_time)


        consent = self.request.get('consent')
        if not consent:
            consent = False

        offer.displayname = self.request.get('displayname')
        offer.text = self.request.get('text')
        offer.seconds = seconds
        offer.consent = consent

        self.redirect('/events')
