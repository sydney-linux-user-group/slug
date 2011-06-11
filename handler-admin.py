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
import event_edit
import event_publish

application = webapp.WSGIApplication(
  [('/event/add', event_edit.EditEvent),
   ('/event/(.*)/edit', event_edit.EditEvent),
   ('/event/(.*)/publish', event_publish.PublishEvent),
   ('/event/(.*)/email', event_publish.SendEmailAboutEvent),
   ],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
