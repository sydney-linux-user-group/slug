#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Helper module for obtaining lists of events"""

import config
config.setup()

from google.appengine.ext import db

import datetime
import models

def get_future_events(year=None, month=None, day=None):
    now = datetime.datetime.now()

    year = year or now.year
    month = month or now.month
    day = day or now.day


    future_events = db.GqlQuery(
        "SELECT * from Event " +
        "WHERE start > DATETIME(:1, :2, :3, 23, 59, 59) " +
        "ORDER BY start", year, month, day).fetch(100)

    return EventList(future_events, "Coming soon")


def get_current_events(year=None, month=None, day=None):
    now = datetime.datetime.now()

    year = year or now.year
    month = month or now.month
    day = day or now.day


    current_events = db.GqlQuery(
        "SELECT * from Event " +
        "WHERE end >= DATETIME(:1, :2, :3, 00, 00, 00) " +
        "AND end <= DATETIME(:1, :2, :3, 23, 59, 59) " +
        "ORDER BY end", year, month, day).fetch(5)

    return EventList(current_events, "Happening today")

def get_next_event(year=None, month=None, day=None, hour=None, minute=None,
        second=None):
    now = datetime.datetime.now()

    year = year or now.year
    month = month or now.month
    day = day or now.day
    hour = hour or now.hour
    minute = minute or now.minute
    second = second or now.second

    next_event = db.GqlQuery(
        "SELECT * from Event " +
        "WHERE start >= DATETIME(:1, :2, :3, :4, :5, :6) " +
        "ORDER BY start", year, month, day, hour, minute, second).get()

    return next_event

def get_event_lists(year=None, month=None, day=None, hour=None, minute=None,
        second=None):

    event_lists = []
    event_lists.append(get_current_events(year, month, day))
    event_lists.append(get_future_events(year, month, day))

    return event_lists

class EventList():
    """A named list of events.

    Arguments:
        events: list of events
        name: a name """

    def __init__(self, events, name):
        self.events = events
        self.name = name
