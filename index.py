#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Simple pages."""

# Python imports
import os

# AppEngine Imports
from google.appengine.ext import webapp

# Our App imports
import events
from utils.render import render as r


class Index(events.Events):
    """Handler for index page."""

    template = "templates/index.html"


class Refresh(webapp.RequestHandler):
    """Handler for a page which causes the parent to refresh.

    Redirect to this page when an iFrame needs the containing page to reload,
    such as after a success login attempt.
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r('templates/refresh.html', {}))


class StaticTemplate(webapp.RequestHandler):
    """Handler which shows a map of how to get to slug."""
    def get(self, filename):
        template = 'templates/%s.html' % filename
        if os.path.exists(template):
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(r(template, {}))
        else:
            self.redirect('/')
