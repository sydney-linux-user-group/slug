#!/usr/bin/python

"""Generate iCal feed based on events in database."""

import config
config.setup()

import pprint
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from pytz.gae import pytz

import datetime
import models
import vobject

class iCal(webapp.RequestHandler):

    def addEventToCal(self, event, cal):
        """Takes a models.Event, addes it to the calendar/

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
        cal_event.add('uid').value = str(event.key())


    def get(self):
        cal = vobject.iCalendar()

        events = models.Event.all()

        for event in events:
            self.addEventToCal(event, cal)

        self.response.out.write(cal.serialize())

