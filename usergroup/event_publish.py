#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

# Python Imports
import logging

# AppEngine Imports
from django import http
from django import shortcuts
from django.views.decorators import http as method
from django.contrib.auth import decorators as auth

# Third Party imports

# Our App imports
from usergroup import models


@auth.login_required
@method.require_POST
def handler_email(request, event_key):
    assert request.user.is_staff

    event = shortcuts.get_object_or_404(models.Event, pk=event_key)

    if request.user.is_staff or event.published:
        return shortcuts.redirect("/events")

    if event.emailed:
        # This is an update
        subject = "Updated: %s " % event.name
    else:
        subject = event.name

    message = mail.EmailMuliAlternatives()
    message.from_email = "committee@slug.org.au"
    message.to = "announce@slug.org.au"
    message.body = event.plaintext
    message.attach_alernative(event.html, "text/html")
    message.send()

    logging.info("Sent email. Subject: %s | To: %s | Body: %s",
            message.subject, message.to, message.body)
    event.emailed = True
    event.save()

    return shortcuts.redirect("/events")


@auth.login_required
@method.require_POST
def handler(request, event_key):
    assert request.user.is_staff

    event = shortcuts.get_object_or_404(models.Event, pk=event_key)

    announcement = models.Announcement(
        created_by=request.user,
        published_by=request.user,
        name=event.name,
        plaintext=event.plaintext,
        html=event.html)
    event.announcement = announcement.save()

    event.published = True
    event.save()

    return shortcuts.redirect('/events')
