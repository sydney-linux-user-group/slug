#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Helper module for obtaining lists of events"""

# Python Imports
import datetime

# Django Imports

# Third Party imports

# Our App imports
from usergroup import models


def get_date(**kw):
    date = datetime.datetime.now()
    date.replace(**kw)
    return date


def get_event_responses(event, user):
    response = None
    guests = []
    if user:
        q = models.Response.objects.all(
                ).filter(event__exact=event
                ).filter(created_by__exact=user)
        for resp in q:
            if not resp.guest:
                response = resp
            else:
                guests.append(resp)
    return response, guests


def get_eventlist_responses(event_list, user):
    events = []
    for event in event_list:
        response, guests = get_event_responses(event, user)
        events.append((event, response, guests))

    return events


def get_future_events(published_only=True, user=None, count=100, **kw):

    q = models.Event.objects.all()
    q = q.filter(start__gte=get_date(**kw))
    if published_only:
        q = q.filter(published__exact=True)
    q = q.order_by('start')

    return EventList(get_eventlist_responses(
            q[0:count], user), "Coming soon")


def get_current_events(published_only=True, user=None, count=5, **kw):

    date = get_date(**kw)

    q = models.Event.objects.all(
            ).filter(
                start__gte=date.replace(hour=0, minute=0, second=0),
                start__lte=date.replace(hour=23, minute=59, second=59)
            ).order_by('end')

    if published_only:
        q = q.filter(published__exact=True)

    return EventList(get_eventlist_responses(
            q[0:count], user), "Happening today")


def get_next_event(**kw):
    date = get_date(**kw)

    q = models.Event.objects.all(
            ).filter(start__gte=get_date(**kw)
            ).filter(published__exact=True
            ).order_by('start')
    if len(q) == 0:
        return "NULL" #Something null
    return q[0:1]


def get_event_lists(published_only=True, user=None, **kw):

    event_lists = []
    event_lists.append(
        get_current_events(published_only, user, **kw))
    event_lists.append(
        get_future_events(published_only, user, **kw))

    return event_lists


class EventList(object):
    """A named list of events.

    Arguments:
        events: list of events
        name: a name """

    def __init__(self, events, name):
        self.events = events
        self.name = name
