#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""OpenID login page"""

import config
config.setup()

# Python imports
import os

# AppEngine Imports
from google.appengine.ext import webapp

# Our App imports
import events
from utils.render import render as r
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    def get(self):
        continue_url = self.request.GET.get('continue')
        openid_url = self.request.GET.get('openid')
        if not openid_url:
            logging.debug("Serving login page for %s", continue_url)
            self.response.out.write(r(
                'third_party/jQueryOpenIdPlugin/Login.xhtml',
                {'continue': continue_url}))
        else:
            self.redirect(users.create_login_url(continue_url, None, openid_url))

application = webapp.WSGIApplication([
    ('/', MainHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

