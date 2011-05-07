#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Third Party imports
import aeoid.middleware



class AdminEvents(webapp.RequestHandler):
    """Handler for creating and editing Event objects."""

    def get(self, key=None):
        self.redirect('/events')


application = webapp.WSGIApplication(
    [('/events/admin', AdminEvents)],
    debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
