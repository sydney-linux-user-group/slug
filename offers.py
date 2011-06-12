#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the offers."""

import config
config.setup()

from google.appengine.api import users
from google.appengine.ext import webapp

import datetime
import models
import offer_lists

from utils.render import render as r


class Offer(webapp.RequestHandler):
    """Handler for display a single offer."""

    def get(self, key=None):
        # We are using locals which confuses pylint.
        # pylint: disable-msg=W0612
        if not key:
            key = self.request.get('id')

        key = long(key)
        offer = models.Offer.get_by_id(key)

        current_user = users.get_current_user()
        response, guests = offer_lists.get_event_responses(event, current_user)

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            'templates/offer.html', locals()))


class Offers(webapp.RequestHandler):
    """Handler for display a table of offers."""

    template = "templates/offers.html"
    published_only = False

    def get(self, year=None, month=None, day=None):
        # We are using locals which confuses pylint.
        # pylint: disable-msg=W0613,W0612
        now = datetime.datetime.now()

        if users.is_current_user_admin():
            published_only = False
        else:
            published_only = True

        current_user = users.get_current_user()

        offers_lists = event_lists.get_event_lists(
                published_only=published_only, user=current_user)

        next_offer = event_lists.get_next_event()

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            self.template, locals()))
