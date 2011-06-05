#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Default handler for admin pages."""

import os
import config
config.setup(os.environ.get('HTTP_HOST', None))

# AppEngine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# OpenID middleware
import aeoid.middleware

# Import the actual handlers
import editevent
import publishevent
import offers

application = webapp.WSGIApplication(
  [('/event/add', editevent.EditEvent),
   ('/event/(.*)/edit', editevent.EditEvent),
   ('/event/(.*)/publish', publishevent.PublishEvent),
   ('/event/(.*)/email', publishevent.SendEmailAboutEvent),
   ('/offer/add', offers.EditOffer),
   ('/offer/(.*)/edit', offers.EditOffer),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
