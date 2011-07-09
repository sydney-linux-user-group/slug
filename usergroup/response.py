#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for dealing with people's RSVPs."""

# Python imports
import logging

# Django Imports
from django import http
from django import shortcuts
from django.views.decorators.http import as method
from django.contrib.auth.decorators import as auth

# Third Party imports


# Our App imports
from usergroup import models
from usergroup import event_lists


@auth.login_required
@method.require_http_methods(["GET", "POST"])
def handler_response(request):
    """Handler for creating and editing Event objects."""

    # /events/<key>/response (GET/POST)
    try:
        unused_events, key, unused_response = request.path_info.split('/')
    except IndexError:
        return shortcuts.redirect('/events')

    event = shortcuts.get_object_or_404(models.Event, pk=key)

    if request.method == 'GET':
        return shortcut.render(request, 'response-show.html', locals())
    elif request.method == 'POST':
        return handler_response_post(request, event)


@auth.login_required
@method.require_POST
def handler_response_get(request, event):
    """Update an RSVP."""

    response, guests = event_lists.get_event_responses(event, request.user)

    # Check if the person is trying to add friends
    try:
        extra_guests = range(
            0, int(request.POST.get('friends', '0'))-len(guests))
    except ValueError:
        extra_guests = []

    if extra_guests:
        httpresponse = http.HttpResponse()
        httpresponse['Content-Type'] = 'text/html'
        httpresponse.write(render(
                'templates/response-friends.html', locals()))
        return

    # Remove the current information
    if response is not None:
        response.delete()
    for guest in guests:
        guest.delete()

    response = models.Response(
            event=event, created_by=request.user, guest=False)
    response.attending = request.POST.get('attending').lower() != 'no'
    response.save()

    logging.info('Response %s created by user %s (email: %s)',
            response.pk, request.user.username, request.user.email)

    guest_names = request.POST.get_list('guest_name')
    guest_emails = request.POST.get_list('guest_email')
    assert len(guest_names) == len(guest_emails)

    for name, email in zip(guest_names, guest_emails):
        name, email = name.strip(), email.strip()
        if not name or not email:
            continue

        response = models.Response(
                event=event, guest=True, created_by=request.user)
        response.attending = True
        response.guest_name = name
        response.guest_email = email
        response.save()

    return shortcuts.redirect('/event/%s/response' % event.pk)
