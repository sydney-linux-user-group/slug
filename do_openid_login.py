#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""OpenID login page"""

import config
config.setup()

# Python imports

# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Our App imports
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    """Handles logins via AppEngine's integrated openid support."""

    def handle_openid(self, continue_url=None, openid_url=None):
        """If openid provided, being the dance; else return the login form."""
        if openid_url:
            self.redirect(users.create_login_url(continue_url, None,
                openid_url))
        else:
            self.response.out.write(template.render(
                'templates/login.html', {'continue': continue_url}))

    def get(self):
        """Serve the login form."""
        continue_url = self.request.get('continue')
        openid_url = self.request.get('openid_identifier')
        self.handle_openid(continue_url, openid_url)

    def post(self):
        """Should have an endpoint now; start the dance"""
        continue_url = self.request.get('continue')
        openid_url = self.request.get('openid_identifier')
        self.handle_openid(continue_url, openid_url)

application = webapp.WSGIApplication([
    ('.*', MainHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

