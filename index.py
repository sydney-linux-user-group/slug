#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Simple pages."""

from google.appengine.ext import webapp
from utils.render import render as r

import events


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


class Map(webapp.RequestHandler):
    """Handler which shows a map of how to get to slug."""
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(r('templates/map.html', {}))
