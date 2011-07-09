#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Simple pages."""

# Python imports

# AppEngine Imports

# Our App imports
from usergroup import events


def handler_index(request):
    """Handler for index page."""
    return event.handler_events(
            request, "templates/index.html", published_default=True)
