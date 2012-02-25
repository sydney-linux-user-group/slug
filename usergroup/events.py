#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the events."""

# Python Imports
import datetime
import logging
import os
import os.path
import traceback
import cStringIO as StringIO

# Django Imports
from django import http
from django import shortcuts
from django import template
from django.views.decorators import http as method
from django.contrib.auth import decorators as auth

# Third Party imports
import datetime_tz
import markdown

# Our App imports
from usergroup import models
from usergroup import offers
from usergroup import event_lists


# We don't want to wrap this line as we use a grep to extract the details
# pylint: disable-msg=C0301
extensions = ['abbr', 'footnotes', 'def_list', 'fenced_code', 'tables', 'subscript', 'superscript', 'slugheader', 'anyurl']


@method.require_GET
def handler_next(request):
    """Figure out the next event, then redirect to it."""
    if event_lists.get_next_event() == "NULL":
        return shortcuts.redirect("/noevent")
    return shortcuts.redirect(event_lists.get_next_event().get_url())


@method.require_http_methods(["GET", "POST"])
def handler_event(request, event_key=None):

    if request.method == 'GET':
        return handler_event_get(request, event_key)
    elif request.method == 'POST':
        return handler_event_post(request, event_key)


@method.require_GET
def handler_event_get(request, event_key=None):
    """Handler for display a single event."""

    # We are using locals which confuses pylint.
    # pylint: disable-msg=W0612

    # /events/<key>
    # /events?id=<key>
    if event_key is None:
        event = shortcuts.get_object_or_404(models.Event, pk=request.GET.get('id', -1))
    else:
        event = shortcuts.get_object_or_404(models.Event, pk=event_key)

    response, guests = event_lists.get_event_responses(event, request.user)

    return shortcuts.render(request, 'event.html', locals())


@auth.login_required
@method.require_POST
def handler_event_post(request, event_key):
    if not event_key or event_key == 'None':
        event = models.Event(created_by=request.user)
    else:
        event = shortcuts.get_object_or_404(models.Event, pk=event_key)

    assert request.user.is_staff

    start_date = datetime_tz.datetime_tz.smartparse(request.REQUEST['start'])
    end_date = datetime_tz.datetime_tz.smartparse(request.REQUEST['end'])

    event.name = request.REQUEST['name']
    event.input = request.REQUEST['input']
    event.start = start_date.asdatetime()
    event.end = end_date.asdatetime()

    event.save()

    # We can't do this template subsitution until we have saved the event.
    try:
        plaintext = str(template.Template(event.input).render(
                        template.Context({
                            'event': event,
                            'request': request,
                            'agenda': offers.get_event_agenda(event)
                        }), ))
        html = markdown.markdown(plaintext, extensions).encode('utf-8')
        event.plaintext = plaintext
        event.html = html
    except Exception:
        sio = StringIO.StringIO()
        traceback.print_exc(file=sio)
        event.plaintext = sio.getvalue()

    logging.debug("e.a %s, e.n %s", event.announcement, event.name)

    event.save()

    return shortcuts.redirect('%s/edit' % event.get_url())


@method.require_GET
def handler_events(
        request, template="events.html", published_default=False, **kw):
    """Handler for display a table of events."""

    for i, w in kw.items():
        if w:
            kw[i] = int(w)
        else:
            del kw[i]

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
