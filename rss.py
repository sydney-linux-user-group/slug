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
import event_lists


# pylint: disable-msg=C0103
class RSSHandler(webapp.RequestHandler):
    """Handler which outputs an RSS feed."""

    def add_event(self, event, rss):
        """Takes a models.Event, adds it to the calendar.

        Arguments:
            event: a models.Event
            cal: an icalendar.Calendar
        """
        syd = pytz.timezone('Australia/Sydney')

        event_url = "%s%s" % ( self.request.host_url, event.get_url() )

        item = rss_gen.RSSItem(title=event.announcement.name)
        item.title = event.announcement.name
        item.link = event_url
        item.description = event.announcement.html
        item.guid = str(event.announcement.key())
        item.pubDate = syd.localize(event.created_on)

        rss.items.append(item)


    def get(self):
        rss = rss_gen.RSS2(title="Slug Meetings",
                link=self.request.host_url,
                description="SLUG's Meetings")

        rss.lastBuildDate = datetime.datetime.utcnow()
        rss.items = []

        future_events = event_lists.get_future_events()
        current_events = event_lists.get_current_events()

        for event in future_events.events:
            self.add_event(event, rss)
        for event in current_events.events:
            self.add_event(event, rss)

        self.response.out.write(rss.to_xml())
