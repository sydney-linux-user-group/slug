#!/usr/bin/python2.5

"""Application for tracking SLUG user group events."""

import config

# AppEngine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# OpenID middleware
import aeoid.middleware

# Import the actual handlers
import index
import response
import events

application = webapp.WSGIApplication(
  [('/', index.Index),
   ('/event/(.*)/response/show',    response.ShowResponsePage),
   ('/event/(.*)/response/friends', response.FriendsResponsePage),
   ('/event/(.*)/response/update',  response.UpdateResponsePage),
   ('/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?', events.Events),
   ('/event[/]?(.*)', events.Event),
   ('/refresh', index.Refresh),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
