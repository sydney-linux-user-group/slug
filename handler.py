#!/usr/bin/python2.5

"""Application for tracking SLUG user group events."""

import config

import pprint
import logging
import events

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import response

from utils.render import render as r

import aeoid.middleware

class IndexPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(r('templates/index.html', {}))


application = webapp.WSGIApplication(
  [('/', IndexPage),
   ('/response/show', response.ShowResponsePage),
   ('/response/add', response.AddResponsePage),
   ('/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?', events.Events),
   ('/event[/]?(.*)', events.Event),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
