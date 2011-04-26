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
import PyRSS2Gen as rss_gen

# Our App imports
import models
import datetime

# pylint: disable-msg=C0103
class rss(webapp.RequestHandler):
    """Handler which outputs an iCal feed."""

    def add_event(self, event, rss):
        """Takes a models.Event, adds it to the calendar.

        Arguments:
            event: a models.Event
            cal: an icalendar.Calendar
        """
        syd = pytz.timezone('Australia/Sydney')

        event_url = "http://signup.slug.org.au/event/%s" % event.key().id()

        item = rss_gen.RSSItem(title=event.name)
        item.title = event.name
        item.link = event_url
        item.description = event.email
        item.guid = str(event.key())
        item.pubDate = syd.localize(event.created_on)

        rss.items.append(item)


    def get(self):
        rss = rss_gen.RSS2(title="Slug Meetings",
                link="http://signup.slug.org.au",
                description="SLUG's Meetings")

        rss.lastBuildDate = datetime.datetime.utcnow()
        rss.items = []

        # FIXME: Should this show *all* events of all time?
        events = models.Event.all().order("created_on")

        for event in events:
            self.add_event(event, rss)

        self.response.out.write(rss.to_xml())
