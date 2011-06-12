#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

# We have functions with loads of arguments.
# pylint: disable-msg=R0913

"""Helper module for obtaining lists of events"""

import config
config.setup()

from google.appengine.ext import db
from aeoid import users as openid

import datetime
import models

def fix_responses(user):
    fedid = user.federated_identity()
    if fedid:
        openid_user_key = openid.UserInfo.get_by_identity_url(fedid)
        query = ("Select * from Response "
                 "WHERE created_by = :1")
        resps = db.GqlQuery(query, openid_user_key)
        for resp in resps:
            resp.gcreated_by = user
            resp.put()

def get_event_responses(event, user):
    response = None
    guests = []
    if user:
        fix_responses(user)
        responses = event.responses.filter("gcreated_by = ",
                user).order("created_on")
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
        events.append( (event, response, guests) )

    return events


def get_future_events(
        year=None, month=None, day=None, published_only=True, user=None,
        count=100):
    now = datetime.datetime.now()

    year = year or now.year
    month = month or now.month
    day = day or now.day

    query = ("SELECT * from Event "
             "WHERE start > DATETIME(:1, :2, :3, 23, 59, 59) ")
    if published_only:
        query += "AND published = True "
    query += "ORDER BY start"

    future_events = db.GqlQuery(query, year, month, day).fetch(count)

    return EventList(get_eventlist_responses(
        future_events, user), "Coming soon")

def get_current_events(
        year=None, month=None, day=None, published_only=True, user=None,
        count=5):
    now = datetime.datetime.now()

    year = year or now.year
    month = month or now.month
    day = day or now.day

    query = ("SELECT * from Event "
             "WHERE end >= DATETIME(:1, :2, :3, 00, 00, 00) "
             "AND end <= DATETIME(:1, :2, :3, 23, 59, 59) ")
    if published_only:
        query += "AND published = True "
    query += "ORDER BY end"

    current_events = db.GqlQuery(query, year, month, day).fetch(count)

    return EventList(get_eventlist_responses(
        current_events, user), "Happening today")

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
        second=None, published_only=True, user=None):

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
