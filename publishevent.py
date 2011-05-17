#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

# Python Imports
import os
import os.path
import traceback
import cStringIO as StringIO
from datetime import datetime

# AppEngine Imports
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Third Party imports
import aeoid.middleware
from dateutil import rrule
from datetime_tz import datetime_tz

# Our App imports
import models
from utils.render import render as r


# We don't want to wrap this line as we use a grep to extract the details
# pylint: disable-msg=C0301
extensions = ['abbr', 'footnotes', 'def_list', 'fenced_code', 'tables', 'subscript', 'superscript', 'slugheader', 'anyurl']

def prep_values(key=None):
    user = users.get_current_user()
    if user is None:
        login_url = users.create_login_url(self.request.path)
        self.redirect(login_url)
        return

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

    return user, event


class SendEmailAboutEvent(webapp.RequestHandler):
    def post(self, key=None):
        user, event = prep_values(key)

        if not event.published:
            self.redirect('/event')

        message = mail.EmailMessage()
        message.sender = "committee@slug.org.au"
        message.to = "announce@slug.org.au"
        message.body = event.plaintext
        message.html = event.html

        if event.emailed:
            # This is an update
            message.subject = "Updated: %s " % event.name
        else:
            message.subject = event.name

        message.send()
        event.put()

        self.redirect("/events")

class PublishEvent(webapp.RequestHandler):
    def post(self, key=None):

        user, event = prep_values(key)

        announcement = models.Announcement(
                name=event.name,
                plaintext=event.plaintext,
                html = event.html)

        event.announcement = announcement.put()

        event.published = True
        event.put()

        self.redirect('/events')



application = webapp.WSGIApplication(
     [('/event/(.*)/publish', PublishEvent),
      ('/event/(.*)/email', SendEmailAboutEvent)],
    debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
