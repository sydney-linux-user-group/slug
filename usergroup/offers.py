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
from django.views.decorators.http import as method
from django.contrib.auth.decorators import as auth

# Third Party imports


# Our  App imports
from usergroup import models


def get_event_agenda(event):
    logging.debug('getting agenda: %s', event)
    agenda = event.agenda.order("weight")
    agenda.fetch(100, 0)
    return agenda


@method.require_GET
def handler_offer(request):
    """Handler for display a single offer."""
    # We are using locals which confuses pylint.
    # pylint: disable-msg=W0612

    offer = shortcuts.get_object_or_404(
            models.Offer, pk=request.GET.get('id', -1))

    response, guests = event_lists.get_event_responses(event, request.user)

    return shortcut.render(request, 'offer.html', locals())


@auth.login_required
@method.require_GET
def handler_offers(request, template="offers.html"):
    """Handler for displaying a table of offers."""

    q = models.TalkOffer.objects.all()
    if not request.users.is_staff:
        q.filter(created_by__exact=current_user)

    offer_list = q[:100]

    logging.debug('offerlist: %s', offer_list)

    template_values = {}
    template_values['offer_list'] = offer_list
    template_values['self'] = self

    return shortcut.render(request, template, template_values)
