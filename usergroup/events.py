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
from django.views.decorators import http as method
from django.contrib.auth import decorators as auth

# Third Party imports


# Our App imports
from usergroup import models
from usergroup import event_lists


def get_event_from_url(request):
    # /events/<key>/<action> (POST)
    try:
        unused_events, key, unused_leftover = request.path_info.split('/')
    except IndexError:
        raise http.Http404

    return shortcuts.get_object_or_404(models.Event, pk=key)


@method.require_GET
def handler_next(request):
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
        unused_events, key = request.path_info.split('/')
    except IndexError:
        key = request.GET.get('id', -1)

    event = shortcuts.get_object_or_404(models.Event, pk=key)

    response, guests = event_lists.get_event_responses(event, request.user)

    return shortcuts.render(request, 'event.html', locals())


@method.require_GET
def handler_events(
        request, template="events.html", published_default=False, **kw):
    """Handler for display a table of events."""

    # We are using locals which confuses pylint.
    # pylint: disable-msg=W0613,W0612

    if request.user.is_staff:
        published_only = published_default
    else:
        published_only = True

    events_lists = event_lists.get_event_lists(
            published_only=published_only, user=request.user, **kw)

    next_event = event_lists.get_next_event()

    return shortcuts.render(request, template, locals())
