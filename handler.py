#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Default handler."""

import config
config.setup()

# AppEngine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# OpenID middleware
import aeoid.middleware

# Import the actual handlers
import index
import response
import events
import ical
import rss

application = webapp.WSGIApplication(
  [('/', index.Index),
   ('/event/(.*)/response/show',    response.ShowResponsePage),
   ('/event/(.*)/response/friends', response.FriendsResponsePage),
   ('/event/(.*)/response/update',  response.UpdateResponsePage),
   ('/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?',
        events.Events),
   ('/event[/]?(.*)', events.Event),
   ('/refresh', index.Refresh),
   ('/map', index.Map),
   ('/ical', ical.iCal),
   ('/rss', rss.rss),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
