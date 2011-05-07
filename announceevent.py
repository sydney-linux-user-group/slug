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
from google.appengine.ext import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Third Party imports
import aeoid.middleware
from dateutil import rrule
from datetime_tz import datetime_tz
import markdown

# Our App imports
import models
from utils.render import render as r


# We don't want to wrap this line as we use a grep to extract the details
# pylint: disable-msg=C0301
extensions = ['abbr', 'footnotes', 'def_list', 'fenced_code', 'tables', 'subscript', 'superscript', 'slugheader', 'anyurl']


class AnnounceEvent(webapp.RequestHandler):
    def post(self, key=None):
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

        message = mail.EmailMessage()
        message.sender = user.email()
        message.to = "slug-sysadmins@groups.google.com"
        message.body = event.plaintext
        message.subject = event.name

        message.send()

        self.redirect('%s/edit' % event.get_url())


application = webapp.WSGIApplication(
     ('/event/(.*)/announce', AnnounceEvent)],
    debug=True)
application = aeoid.middleware.AeoidMiddleware(application)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
