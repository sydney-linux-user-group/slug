#!/usr/bin/python2.5

"""Application for tracking SLUG user group events."""

import config

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
      'templates/Event.html', { 'event': event}))

class Events(webapp.RequestHandler):

  def get(self, year=None, month=None, day=None):

    now = datetime.datetime.now()

    future_events = db.GqlQuery(
      "SELECT * from Event " + 
      "WHERE start >= DATE(:1, :2, :3) " + 
      "ORDER BY start", now.year, now.month, now.day)
    
    current_events = db.GqlQuery(
      "SELECT * from Event " + 
      "WHERE end >= DATETIME(:1, :2, :3, 00, 00, 00) " + 
      "AND end <= DATETIME(:1, :2, :3, 23, 59, 59) " +
      "ORDER BY end", now.year, now.month, now.day)

    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(r(
      'templates/Events.html', 
      {'future_events': future_events, 'current_events': current_events}))

  def post(self, urltail):
   event = models.Event(name = self.request.get('name'),
                        text = self.request.get('text'),
                        start = datetime.datetime.now(),
                        end = datetime.datetime.now(),
                       )
   event.put()
   self.redirect('/event/%d' % event.key().id())
