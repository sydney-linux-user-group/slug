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

class Event(webapp.RequestHandler):
    """Handler for display a single event."""

    def get(self, key=None):
        if not key:
            key = self.request.get('id')

        key = long(key)
        event = models.Event.get_by_id(key)

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            'templates/event.html', { 'event': event}))


class Events(webapp.RequestHandler):
    """Handler for display a table of events."""

    template = "templates/events.html"

    def get(self, year=None, month=None, day=None):
        now = datetime.datetime.now()

        year = self.request.get('year', now.year)
        month = self.request.get('month', now.month)
        day = self.request.get('day', now.day)

        future_events = db.GqlQuery(
            "SELECT * from Event " +
            "WHERE start > DATETIME(:1, :2, :3, 23, 59, 59) " +
            "ORDER BY start", year, month, day).fetch(100)

        current_events = db.GqlQuery(
            "SELECT * from Event " +
            "WHERE end >= DATETIME(:1, :2, :3, 00, 00, 00) " +
            "AND end <= DATETIME(:1, :2, :3, 23, 59, 59) " +
            "ORDER BY end", year, month, day).fetch(5)

        next_event = (len(current_events) and current_events[0]
                      or (len(future_events) and future_events[0]))

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r(
            self.template,
            {'future_events': future_events, 'current_events': current_events,
             'next_event': next_event}))
