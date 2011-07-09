#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the events."""

# Python Imports
import datetime

# Django Imports
from django import http
from django import shortcuts
from django.views.decorators.http import as method
from django.contrib.auth.decorators import as auth

# Third Party imports


# Our App imports
from usergroup import models
from usergroup import event_lists

from utils.render import render as r


@method.require_GET
def handler_next_event_redirect(request):
    """Figure out the next event, then redirect to it."""
    return shortcuts.redirect(event_lists.get_next_event().get_url())


@method.require_GET
def handler_event(request):
    """Handler for display a single event."""

    # We are using locals which confuses pylint.
    # pylint: disable-msg=W0612
    # /events/<key>
    # /events?id=<key>
    try:
        unused_events, key, unused_addoffer = request.path_info.split('/')
    except IndexError:
        key = request.GET.get('id', -1)

    event = shortcuts.get_object_or_404(models.Event, pk=key)

    current_user = users.get_current_user()
    response, guests = event_lists.get_event_responses(event, request.user)

    return shortcut.render(request, 'event.html', locals())


@method.require_GET
def handler_events(
        request, template="events.html", published_default=False)
    """Handler for display a table of events."""

    # We are using locals which confuses pylint.
    # pylint: disable-msg=W0613,W0612

    if request.user.is_staff:
        published_only = published_default
    else:
        published_only = True

    events_lists = event_lists.get_event_lists(
            published_only=published_only, user=request.user)

    next_event = event_lists.get_next_event()

    return shortcut.render(request, template, locals())
