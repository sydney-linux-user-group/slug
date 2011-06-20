#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

import logging
import re

# AppEngine Imports
from google.appengine.api import users
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
                self.redirect('/offers')
                return
        else:
            offer = None

        q = models.TalkOffer.all()
        if not users.is_current_user_admin():
            q.filter("created_by =", user)

        offer_list = q.fetch(limit=100)

        self.response.out.write(r(
            'templates/offertalk.html', { 'offer': offer,
                'offer_list': offer_list, 'self': self }
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
            logging.debug('creating offer')
            offer = models.TalkOffer(title=self.request.get('title'))

        valid = True

        if self.request.get('consent'):
            consent = True
        else:
            consent = False

        offer.displayname = self.request.get('displayname')
        offer.text = self.request.get('text')
        minutes = self.request.get('minutes')
        if minutes.isnumeric():
            offer.minutes = int(minutes)
        else:
            mins = ''.join(re.findall('[0-9]+', minutes))
            if mins.isnumneric():
                offer.minutes = int(mins)

        offer.consent = consent
        offer.put()

        logging.debug('TalkOffer created by %s (%s email: %s fedid: %s) - : %s',
                offer.displayname, user.nickname(), user.email(),
                user.federated_identity(), offer.title)
        logging.debug('For talkoffer %s, %s gave displayname %s. '
                'Consent flag is: %s', offer.title, user.nickname(),
                offer.displayname, offer.consent)

        self.redirect('/offer/add#prevoffers')
