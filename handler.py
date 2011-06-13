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

# Import the actual handlers
import index
import response
import events
import offer_edit
import ical
import rss

application = webapp.WSGIApplication(
  [('/', index.Index),
   ('/event/next', events.Next),
   ('/ical[/]?(?P<key>[^\.]*)(?:.ics)?', ical.iCal),
   ('/event[/]?(?P<key>[^\.]*)(?:.ics)', ical.iCal),
   ('/event/ical', ical.iCal),
   ('/rss', rss.RSSHandler),
   ('/\d*/.*feed.*', rss.RSSHandler),
   ('/full/.*feed.*', rss.RSSHandler),
   ('/event/.*feed.*', rss.RSSHandler),
   ('/event/(.*)/response/show',    response.ShowResponsePage),
   ('/event/(.*)/response/update',  response.UpdateResponsePage),
   ('/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?',
        events.Events),
   ('/event/(.*)', events.Event),
   ('/offer/(.*)/edit', offer_edit.EditOffer),
   ('/offer/add', offer_edit.EditOffer),
   ('/refresh', index.Refresh),
   ('/(.*)', index.StaticTemplate),
   ],
  debug=True)

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
