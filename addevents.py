#!/usr/bin/python2.5

"""Application for tracking SLUG user group events."""

import config

import pprint
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


import models
import datetime

import aeoid.middleware

import dateutil
import datetime_tz

from utils.render import render as r

class Add(webapp.RequestHandler):

  def get(self, year=None, month=None, day=None):

    self.response.out.write(r('templates/addevents.html', {}))

  def post(self, urltail):
    start_date = datetime_tz.smart_parse(self.request.get('start'))
    end_date = datetime_tz.smart_parse(self.request.get('end'))
    event = models.Event(name = self.request.get('name'),
                         text = self.request.get('text'),
                         start = start_date,
                         end = end_date,
                        )
    event.put()
    self.redirect('/event/%d' % event.key().id())

application = webapp.WSGIApplication(
  [('/events/add', Add), ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
