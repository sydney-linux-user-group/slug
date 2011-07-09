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
import event_lists


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
        cal_event.add('summary').value = event.announcement.name
        cal_event.add('dtstart').value = syd.localize(event.start)
        cal_event.add('dtend').value = syd.localize(event.end)
        cal_event.add('dtstamp').value = syd.localize(event.created_on)
        cal_event.add('description').value = event.announcement.plaintext or \
          'See %s%s for details' % ( self.request.host_url, event.get_url() )
        cal_event.add('uid').value = str(event.announcement.key())


    def get(self, key=None):
        """If a key is passed, return just that Event, else whole calendar."""

        cal = vobject.iCalendar()

        if key:
            event = models.Event.get_by_id(int(key))
            self.add_event(event, cal)
        else:
            future_events = event_lists.get_future_events()
            current_events = event_lists.get_current_events()

            for event, _, _ in current_events.events:
                self.add_event(event, cal)
            for event, _, _ in future_events.events:
                self.add_event(event, cal)

        self.response.headers['Content-Type'] = 'text/x-vCalendar'
        self.response.out.write(cal.serialize())
