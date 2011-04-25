#!/usr/bin/python

"""Generate iCal feed based on events in database."""

import config
import pprint
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import datetime
import icalendar
import models
from pytz.gae import pytz

class iCal(webapp.RequestHandler):

    def addEventToCal(self, event, cal):
        """Takes a models.Event, addes it to the calendar/

        Arguments:
            event: a models.Event
            cal: an icalendar.Calendar
        """
        syd = pytz.timezone('Australia/Sydney')

        cal_event = icalendar.Event()
        cal_event.add('summary', event.name)
        cal_event.add('dtstart', syd.localize(event.start))
        cal_event.add('dtend', syd.localize(event.end))
        cal_event.add('dtstamp', syd.localize(event.created_on))
        cal_event.add('uid', event.key())
        cal_event.add('priority', 5)

        cal.add_component(cal_event)


    def get(self):
        cal = icalendar.Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', 'SLUG Event System//signup.slug.org.au//')

        events = models.Event.all()

        for event in events:
            self.addEventToCal(event, cal)

        self.response.out.write(cal.as_string())

