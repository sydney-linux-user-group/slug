#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

# Python imports
import logging
import re

# django Imports
from django import http
from django import shortcuts
from django.views.decorators.http import as method
from django.contrib.auth.decorators import as auth

# Third Party imports


# Our App imports
from usergroup import models


@auth.login_required
@method.require_http_methods(["GET", "POST"])
def handler(request):
    """Handler for creating and editing Event objects."""

    q = models.TalkOffer.objects.all()
    if not request.user.is_staff():
        q.filter(created_by__exact=request.user)
    offers = q[:100]

    # /offer/<key> (POST/Get)
    # /offer/add (POST/Get)
    try:
        unused_offer, key = request.path_info.split('/')
    except IndexError:
        return shortcuts.redirect('/offers')

    if key == 'add':
        offer = models.Offer()
    else:
        offer = shortcuts.get_object_or_404(models.TalkOffer, pk=key)

    if request.method == 'GET':
        offer_list = q[:100]

        return shortcut.render(
                'offertalk.html', {
                        'offer': offer, 'offer_list': offers, 'self': self})
    elif request.method == 'POST':
        return handler_edit(request, offer, offers)


@auth.login_required
@method.require_POST
def handler_edit(request, offer, offers):

    valid = True

    if request.GET['consent']:
        consent = True
    else:
        consent = False

    offer.displayname = request.GET['displayname']
    offer.text = request.GET['text']
    offer.contactinfo = request.GET['contactinfo']

    minutes = request.GET['minutes']
    if minutes.isnumeric():
        offer.minutes = int(minutes)
    else:
        mins = ''.join(re.findall('[0-9]+', minutes))
        if mins.isnumneric():
            offer.minutes = int(mins)

    offer.consent = consent
    offer.put()

    logging.debug('TalkOffer created by %s (%s email: %s fedid: %s) - : %s',
                  offer.displayname, request.user.username, request.user.email,
                  offer.title)
    logging.debug('For talkoffer %s, %s gave displayname %s. '
                  'Consent flag is: %s', offer.title, user.username,
                  offer.displayname, offer.consent)

    return shortcuts.redirect('/offers')
