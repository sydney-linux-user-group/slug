#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the events."""

import config
config.setup()

from google.appengine.ext import db
from google.appengine.ext import webapp

import datetime
import models

from utils.render import render as r
from utils import events_helper as e

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

        year = self.request.get('year', now.year)
        month = self.request.get('month', now.month)
        day = self.request.get('day', now.day)

        future_events = e.get_future_events(year, month, day)
        current_events = e.get_current_events(year, month, day)
        next_event = e.get_next_event(year, month, day)


        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            self.template, locals()))
