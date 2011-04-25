#!/usr/bin/python

from google.appengine.ext import webapp
from utils.render import render as r


import events


class Index(events.Events):
  template = "templates/index.html"


class Refresh(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(r('templates/refresh.html', {}))


class Map(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(r('templates/map.html', {}))
