#!/usr/bin/python

"""Application for tracking SLUG user group events."""

import config
config.setup()

import pprint
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

import models
import datetime

from utils.render import render as r

class Event(webapp.RequestHandler):
  def get(self, id=None):
    if not id:
      id = self.request.get('id')

    id = long(id)
    event = models.Event.get_by_id(id)

    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(r(
      'templates/event.html', { 'event': event}))


class Events(webapp.RequestHandler):
  template = "templates/events.html"

  def get(self):
    now = datetime.datetime.now()

    future_events = db.GqlQuery(
      "SELECT * from Event " +
      "WHERE start > DATETIME(:1, :2, :3, 23, 59, 59) " +
      "ORDER BY start", now.year, now.month, now.day).fetch(100)

    current_events = db.GqlQuery(
      "SELECT * from Event " +
      "WHERE end >= DATETIME(:1, :2, :3, 00, 00, 00) " +
      "AND end <= DATETIME(:1, :2, :3, 23, 59, 59) " +
      "ORDER BY end", now.year, now.month, now.day).fetch(5)

    next_event = len(current_events) and current_events[0] or future_events[0]

    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(r(
      self.template,
      {'future_events': future_events, 'current_events': current_events,
       'next_event': next_event}))
