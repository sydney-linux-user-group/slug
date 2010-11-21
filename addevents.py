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

from utils.render import render as r

class Add(webapp.RequestHandler):

  def get(self, year=None, month=None, day=None):

    self.response.out.write(r('templates/addevents.html', {}))

  def post(self, urltail):
   event = models.Event(name = self.request.get('name'),
                        text = self.request.get('text'),
                        start = datetime.datetime.now(),
                        end = datetime.datetime.now(),
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
