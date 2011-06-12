#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""OpenID login page"""

import config
config.setup()

# Python imports
import logging
import os

# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Our App imports
import events
from utils.render import render as r
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    def handle_openid(self, continue_url=None, openid_url=None):
        if not openid_url:
            logging.debug("Serving login page for %s", continue_url)
            self.response.out.write(template.render(
                'templates/login.html', {'continue': continue_url}))
        else:
            self.redirect(users.create_login_url(continue_url, None, openid_url))

    def get(self):
        continue_url = self.request.GET.get('continue')
        openid_url = self.request.GET.get('openid')
        self.handle_openid()

    def post(self):
        logging.debug(self.request.GET.get())
        continue_url = self.request.GET.get('continue')
        openid_url = self.request.GET.get('openid')
        self.handle_openid()
        

application = webapp.WSGIApplication([
    ('.*', MainHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

