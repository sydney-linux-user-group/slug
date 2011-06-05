#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

# Python Imports
from datetime import datetime

# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django import template

# Third Party imports
import aeoid.middleware

# Our App imports
import models
from utils.render import render as r


class EditOffer(webapp.RequestHandler):
    """Handler for creating and editing Event objects."""

    def get(self, key=None):
        if key:
            try:
                key = long(key)
                offer = models.TalkOffers.get_by_id(key)
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
        if key:
            try:
                key = long(key)
                offer = models.TalkOffer.get_by_id(key)
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/events')
                return
        else:
            offer = models.TalkOffer(name=self.request.get('name'))

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

        offer.text = self.request.get('text')
        offer.seconds = seconds
        offer.consent = consent

        offer.put()

        self.redirect('/events')


application = webapp.WSGIApplication(
    [('/offer/add', EditOffer),
     ('/offer/(.*)/edit', EditOffer)],
    debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
