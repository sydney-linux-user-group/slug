#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

# Python Imports
import os
import simplejson
from datetime import datetime

# Django Imports
from django import http
from django import shortcuts
from django.views.decorators import http as method
from django.contrib.auth import decorators as auth

# Third Party imports
from dateutil import rrule
from datetime_tz import datetime_tz

# Our App imports
from usergroup import models
from usergroup import offers


def lastfridays():
    """Return 5 last Fridays of the month."""
    return list(x.date() for x in rrule.rrule(
         rrule.MONTHLY, interval=1, count=10, byweekday=(rrule.FR(-1)),
         dtstart=datetime.now()))


def get_templates():
    """Get all the markdown templates."""
    ret = []

    directory = "usergroup/templates/markdown"
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue

        fullpath = os.path.join(directory, filename)
        name = filename.replace('.md', '')
        ret.append((name, file(fullpath).read()))
    return ret


@auth.login_required
@method.require_POST
def handler_offer_add(request, event_key):
    """Adds an offer to an event"""

    event = shortcuts.get_object_or_404(models.Event, pk=event_key)
    offer = shortcuts.get_object_or_404(
            models.TalkOffer, pk=request.POST.get('id', -1))

    talk = models.LightningTalk(event=event, offer=offer)
    talk.save()

    response = http.HttpResponse()
    response['Content-Type'] = 'application/javascript'
    response.write(simplejson.dumps({'key': str(talk.key())}))
    return response


@auth.login_required
@method.require_POST
def handler_offer_remove(request, event_key):
    """Removes an offer from an event."""

    event = shortcuts.get_object_or_404(models.Event, pk=event_key)
    talk = shortcuts.get_object_or_404(
            models.LightningTalk, pk=request.POST.get('id', -1))
    assert talk.event == event

    talk.delete()

    response = http.HttpResponse()
    response['Content-Type'] = 'application/javascript'
    response.write(simplejson.dumps({'deleted': str(True)}))
    return response


@auth.login_required
@method.require_GET
def handler(request, event_key):
    """Handler for viewing the edit form."""

    assert request.user.is_staff

    try:
        if event_key == 'add':
            event = models.Event(created_by=request.user)
        else:
            event = shortcuts.get_object_or_404(models.Event, pk=event_key)
    except IndexError:
        return shortcuts.redirect('/events')

    template_values = {}
    if event:
        template_values['agenda'] = offers.get_event_agenda(event)
    else:
        template_values['agenda'] = None

    template_values['event'] = event
    template_values['fridays'] = lastfridays()
    template_values['templates'] = get_templates()
    template_values['offers'] = models.TalkOffer.objects.all()[:100]

    return shortcuts.render(
            request, 'editevent.html', template_values)
