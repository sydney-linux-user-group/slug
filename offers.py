#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the offers."""

import config
config.setup()

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp

import datetime
import logging
import models

from utils.render import render as r


def get_event_agenda(event):
    logging.debug('getting agenda: %s', event)
    agenda = event.agenda.order("weight")
    agenda.fetch(100, 0)
    return agenda

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
    """Handler for displaying a table of offers."""

    template = "templates/offers.html"

    def get(self, limit=100, offset=0):
        current_user = users.get_current_user()
        if not current_user:
            self.redirect('/_ah/login_required?continue=%s' % self.request.path)
            return

        q = models.TalkOffer.all()
        if not users.is_current_user_admin():
            q.filter("created_by =", current_user)

        offer_list = q.fetch(limit=limit, offset=offset)

        logging.debug('offerlist: %s', offer_list)

        template_values = {}
        template_values['offer_list'] = offer_list
        template_values['self'] = self

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            self.template, template_values))
