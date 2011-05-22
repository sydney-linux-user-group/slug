#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Default handler."""

import os
import config
config.setup(os.environ.get('HTTP_HOST', None))

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
    ('/event/next', events.Next),
   ('/event/(.*)/response/show',    response.ShowResponsePage),
   ('/event/(.*)/response/update',  response.UpdateResponsePage),
   ('/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?',
        events.Events),
   ('/ical[/]?(?P<key>[^\.]*)(?:.ics)?', ical.iCal),
   ('/event[/]?(?P<key>[^\.]*)(?:.ics)', ical.iCal),
   ('/event[/]?(.*)', events.Event),
   ('/refresh', index.Refresh),
   ('/rss', rss.RSSHandler),
   ('/(.*)', index.StaticTemplate),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
