#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Generate RSS feed based on events in database."""

# Python imports
import datetime

# AppEngine Imports
from django import http
from django import shortcuts
from django.views.decorators.http import as require

# Third Party imports
from pytz.gae import pytz
import PyRSS2Gen as rss_gen

# Our App imports
from usergroup import event_lists


def add_event(host_url, event, rss):
    """Takes a models.Event, adds it to the calendar.

    Arguments:
        event: a models.Event
        cal: an icalendar.Calendar
    """
    syd = pytz.timezone('Australia/Sydney')

    event_url = "%s%s" % (host_url, event.get_url() )

    item = rss_gen.RSSItem(title=event.announcement.name)
    item.title = event.announcement.name
    item.link = event_url
    item.description = event.announcement.html
    item.guid = str(event.announcement.key())
    item.pubDate = syd.localize(event.created_on)

    rss.items.append(item)


@require.require_GET
def handler_rss(request):
    """Handler which outputs an RSS feed."""

    rss = rss_gen.RSS2(title="Slug Meetings",
            link=self.request.host_url,
            description="SLUG's Meetings")

    rss.lastBuildDate = datetime.datetime.utcnow()
    rss.items = []

    future_events = event_lists.get_future_events()
    current_events = event_lists.get_current_events()

    for event, _, _ in future_events.events:
        self.add_event(request.get_host(), event, rss)
    for event, _, _ in current_events.events:
        self.add_event(request.get_host(), event, rss)

    response = http.HttpResponse()
    response['Content-Type'] = 'application/rss+xml'
    response.write(rss.to_xml())
    return response
