#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the events."""

import config
config.setup()

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp

import datetime
import logging
import models
import event_lists

from utils.render import render as r

class Next(webapp.RequestHandler):
    """Figure out the next event, then redirect to it."""
    def get(self):
        self.redirect(event_lists.get_next_event().get_url())

class Event(webapp.RequestHandler):
    """Handler for display a single event."""

    def get(self, key=None):
        if not key:
            key = self.request.get('id')

        key = long(key)
        event = models.Event.get_by_id(key)

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            'templates/event.html', locals()))


class Events(webapp.RequestHandler):
    """Handler for display a table of events."""

    template = "templates/events.html"

    def get(self, year=None, month=None, day=None):
        now = datetime.datetime.now()

        if users.is_current_user_admin():
            events_lists = event_lists.get_event_lists(published=False)
        else:
            events_lists = event_lists.get_event_lists()

        next_event = event_lists.get_next_event()

        logging.debug("events_lists: %s", events_lists)

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            self.template, locals()))
