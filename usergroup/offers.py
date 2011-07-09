#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for viewing the offers."""

# Python imports
import logging
import datetime

# django imports
from django import http
from django import shortcuts
from django.views.decorators import http as method
from django.contrib.auth import decorators as auth

# Third Party imports


# Our  App imports
from usergroup import models


def get_event_agenda(event):
    logging.debug('getting agenda: %s', event)
    agenda = event.agenda.order_by("weight")
    return agenda[:100]


@auth.login_required
@method.require_GET
def handler(request, template="offers.html"):
    """Handler for displaying a table of offers."""

    q = models.TalkOffer.objects.all()
    if not request.users.is_staff:
        q = q.filter(created_by__exact=current_user)

    offer_list = q[:100]

    logging.debug('offerlist: %s', offer_list)

    template_values = {}
    template_values['offer_list'] = offer_list
    template_values['self'] = self

    return shortcut.render(request, template, template_values)
