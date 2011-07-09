#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Generate iCal feed based on events in database."""

# Python Imports


# Django Imports
from django import http
from django import shortcuts
from django.views.decorators import http as method

# Third Party imports
import pytz
import vobject

# Our App imports
from usergroup import models
from usergroup import event_lists


def add_event(host_url, event, cal):
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
      'See %s%s for details' % (host_url, event.get_url() )
    cal_event.add('uid').value = str(event.announcement.key())


@method.require_GET
def handler(request):
    """Handler which outputs an iCal feed."""

    cal = vobject.iCalendar()

    # /ical/<key>
    try:
        # If a key is passed, return just that Event
        unused_ical, key = request.path_info.split('/')

        event = shortcuts.get_object_or_404(models.Event, pk=key)
        self.add_event(request.get_host(), event, cal)
    except IndexError:
        # else whole calendar.
        future_events = event_lists.get_future_events()
        current_events = event_lists.get_current_events()

        for event, _, _ in current_events.events:
            self.add_event(request.get_host(), event, cal)
        for event, _, _ in future_events.events:
            self.add_event(event, cal)

    response = http.HttpResponse()
    response['Content-Type'] = 'text/x-vCalendar'
    response.write(cal.serialize())
    return response
