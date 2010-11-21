#!/usr/bin/python2.5

"""Application for tracking SLUG user group events."""

import config

import pprint
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

import models
import datetime


class Event(webapp.RequestHandler):
  def get(self, id):
    id = long(id)
    event = models.Event.get_by_id(id)
    #event = models.Event.get_by_key_name('ahdzeWRuZXktbGludXgtdXNlci1ncm91cHILCxIFRXZlbnQYAQw')

    template_values = {
      'key': id,
      'name': event.name,
      'text': event.text,
    }

    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render(
      'templates/Event.html', template_values))

class Events(webapp.RequestHandler):

  @login_required
  def get(self, urltail):
    urltail = urltail.lstrip('/')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render(
      'templates/Events.html', {'urltail': urltail}))

  def post(self, urltail):
   event = models.Event(name = self.request.get('name'),
                        text = self.request.get('text'),
                        start = datetime.datetime.now(),
                        end = datetime.datetime.now(),
                       )
   event.put()
   self.redirect('/event/%d' % event.key().id())
