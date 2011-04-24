#!/usr/bin/python

"""Application for tracking SLUG user group events."""

import config

import pprint
import logging
import events
import ical

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
   ('/event/(.*)/response/show',    response.ShowResponsePage),
   ('/event/(.*)/response/friends', response.FriendsResponsePage),
   ('/event/(.*)/response/update',  response.UpdateResponsePage),
   ('/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?', events.Events),
   ('/event[/]?(.*)', events.Event),
   ('/ical', ical.iCal),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
