#!/usr/bin/python

"""Application for tracking SLUG user group events."""

import config
config.setup()

# Python Imports
import pprint
import logging
import cStringIO as StringIO
from datetime import datetime

# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django import template

# Third party imports
import aeoid.middleware
import dateutil
from dateutil import rrule
from datetime_tz import datetime_tz
import markdown

# Our App imports
import models
from utils.render import render as r


class EditEvent(webapp.RequestHandler):

  def lastfridays(self):
    """Return 5 last Fridays of the month."""
    return list(x.date() for x in rrule.rrule(
       rrule.MONTHLY, interval=1, count=10, byweekday=(rrule.FR(-1)),
       dtstart=datetime.now()))

  def get(self, id=None):
    if id:
      try:
        id = long(id)
        event = models.Event.get_by_id(id)
        assert event
      except:
        self.redirect('/events')
        return
    else:
      event = None
    
    fridays = self.lastfridays()

    self.response.out.write(r(
        'templates/editevent.html', {'event': event, 'fridays': fridays})
    )

  def post(self, id=None):
    if id:
      try:
      	id = long(id)
        event = models.Event.get_by_id(id)
      except:
        self.redirect('/events')
        return
    else:
      event = models.Event(name='', text='', html='', start=datetime.now(), end=datetime.now())

    input = self.request.get('input')
    email = str(template.Template(input).render(template.Context({'event': event})))
    html = markdown.markdown(email).encode('utf-8')

    start_date = datetime_tz.smartparse(self.request.get('start'))
    end_date = datetime_tz.smartparse(self.request.get('end'))

    event.name = self.request.get('name')
    event.input = input
    event.email = email
    event.html = html
    event.start = start_date.asdatetime()
    event.end = end_date.asdatetime()
    event.put()
    if not id:
        id = event.key().id()

    self.redirect('/event/%d/edit' % id)


application = webapp.WSGIApplication(
  [('/event/add', EditEvent),
   ('/event/(.*)/edit', EditEvent)],
  debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
