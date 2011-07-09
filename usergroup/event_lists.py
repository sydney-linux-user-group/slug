#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

# We have functions with loads of arguments.
# pylint: disable-msg=R0913

"""Helper module for obtaining lists of events"""

from usergroup import models


def get_date(**kw):
    date = datetime.datetime.now()
    date.replace(**kw)
    return date


def get_event_responses(event, user):
    response = None
    guests = []
    if user:
        responses = models.Response.objects.all()
        responses.filter(event__extact=event)
        responses.filter(created_by__extact=user)
        for resp in responses:
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

    events = models.Event.objects.all()
    events.filter(start__gte=get_date(**kw))
    if published_only:
        events.filter(published__exact=True)
    events.order_by('start')

    future_events = events[0:count]

    return EventList(get_eventlist_responses(
        future_events, user), "Coming soon")


def get_current_events(published_only=True, user=None, count=5, **kw):

    date = get_date(**kw)

    events = models.Event.objects.all()
    events.filter(start__gte=date.replace(hour=0, minute=0, second=0))
    events.filter(start__lte=date.replace(hour=23, minute=59, second=59))
    if published_only:
        events.filter(published__exact=True)
    events.order_by('end')

    current_events = events[0:count]

    return EventList(get_eventlist_responses(
        current_events, user), "Happening today")


def get_next_event(**kw):

    date = get_date(**kw)

    events = models.Event.objects.all()
    events.filter(start__gte=get_date(**kw))
    events.filter(published__exact=True)
    events.order_by('start')

    return events[0:1]


def get_event_lists(published_only=True, user=None):

    event_lists = []
    event_lists.append(
        get_current_events(year, month, day, published_only, user))
    event_lists.append(
        get_future_events(year, month, day, published_only, user))

    return event_lists


class EventList(object):
    """A named list of events.

    Arguments:
        events: list of events
        name: a name """

    def __init__(self, events, name):
        self.events = events
        self.name = name
