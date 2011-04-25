#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

# Python Imports
from datetime import datetime

# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django import template

# Third Party imports
import aeoid.middleware
from dateutil import rrule
from datetime_tz import datetime_tz
import markdown

# Our App imports
import models
from utils.render import render as r


def lastfridays():
    """Return 5 last Fridays of the month."""
    return list(x.date() for x in rrule.rrule(
         rrule.MONTHLY, interval=1, count=10, byweekday=(rrule.FR(-1)),
         dtstart=datetime.now()))


class EditEvent(webapp.RequestHandler):
    """Handler for creating and editing Event objects."""

    def get(self, key=None):
        if key:
            try:
                key = long(key)
                event = models.Event.get_by_id(key)
                assert event
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/events')
                return
        else:
            event = None

        fridays = lastfridays()

        self.response.out.write(r(
            'templates/editevent.html',
            {'event': event, 'fridays': fridays}
            ))

    def post(self, key=None):
        if key:
            try:
                key = long(key)
                event = models.Event.get_by_id(key)
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/events')
                return
        else:
            event = models.Event(name='', text='', html='',
                                 start=datetime.now(), end=datetime.now())

        inputtext = self.request.get('input')
        email = str(template.Template(inputtext).render(
            template.Context({'event': event})))
        html = markdown.markdown(email).encode('utf-8')

        start_date = datetime_tz.smartparse(self.request.get('start'))
        end_date = datetime_tz.smartparse(self.request.get('end'))

        event.name = self.request.get('name')
        event.input = inputtext
        event.email = email
        event.html = html
        event.start = start_date.asdatetime()
        event.end = end_date.asdatetime()
        event.put()
        if not key:
            key = event.key().id()

        self.redirect('/event/%d/edit' % key)


application = webapp.WSGIApplication(
    [('/event/add', EditEvent),
     ('/event/(.*)/edit', EditEvent)],
    debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
