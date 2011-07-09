#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Simple pages."""

# Python imports
import os

# AppEngine Imports
from google.appengine.ext import webapp

# Our App imports
import events
from utils.render import render as r


class Index(events.Events):
    """Handler for index page."""
    published_only = True
    template = "templates/index.html"
