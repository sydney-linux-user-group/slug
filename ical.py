#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Generate iCal feed based on events in database."""

import config
config.setup()

# AppEngine Imports
from google.appengine.ext import webapp

# Third Party imports
from pytz.gae import pytz
import vobject

# Our App imports
import models


# pylint: disable-msg=C0103
class iCal(webapp.RequestHandler):
    """Handler which outputs an iCal feed."""

    def add_event(self, event, cal):
        """Takes a models.Event, adds it to the calendar.

        Arguments:
            event: a models.Event
            cal: an icalendar.Calendar
        """
        syd = pytz.timezone('Australia/Sydney')

        cal_event = cal.add('vevent')
        cal_event.add('summary').value = event.name
        cal_event.add('dtstart').value = syd.localize(event.start)
        cal_event.add('dtend').value = syd.localize(event.end)
        cal_event.add('dtstamp').value = syd.localize(event.created_on)
        cal_event.add('description').value = event.input
        cal_event.add('uid').value = str(event.key())


    def get(self):
        cal = vobject.iCalendar()

        # FIXME: Should this show *all* events of all time?
        events = models.Event.all()

        for event in events:
            self.add_event(event, cal)

        self.response.out.write(cal.serialize())
