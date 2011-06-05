#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

# Python Imports

# AppEngine Imports
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp

# Third Party imports

# Our App imports
import models
import logging


# We don't want to wrap this line as we use a grep to extract the details
# pylint: disable-msg=C0301
extensions = ['abbr', 'footnotes', 'def_list', 'fenced_code', 'tables', 'subscript', 'superscript', 'slugheader', 'anyurl']

def prep_values(key=None):
    user = users.get_current_user()

    if key:
        try:
            key = long(key)
            event = models.Event.get_by_id(key)
            assert event
        # pylint: disable-msg=W0702
        except (AssertionError, ValueError):
            event = None
    else:
        event = None

    return user, event


class SendEmailAboutEvent(webapp.RequestHandler):
    def post(self, key=None):
        user, event = prep_values(key)

        if not user or not event or event.published:
            self.redirect("/events")

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
        logging.info("Sent email. Subject: %s | To: %s | Body: %s",
                message.subject, message.to, message.body)
        event.put()

        self.redirect("/events")


class PublishEvent(webapp.RequestHandler):
    def post(self, key=None):
        user, event = prep_values(key)

        if user and event:
            announcement = models.Announcement(
                name=event.name,
                plaintext=event.plaintext,
                html=event.html)

            event.announcement = announcement.put()

            event.published = True
            event.put()

        self.redirect('/events')
