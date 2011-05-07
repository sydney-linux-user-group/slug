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

    return future_events


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

    return current_events

def get_next_event(year=None, month=None, day=None):
    now = datetime.datetime.now()

    year = year or now.year
    month = month or now.month
    day = day or now.day
    hour = now.hour
    minute = now.minute
    second = now.second


    next_event = db.GqlQuery(
        "SELECT * from Event " +
        "WHERE start >= DATETIME(:1, :2, :3, :4, :5, :6) " +
        "ORDER BY start", year, month, day, hour, minute, second).get()

    return next_event

