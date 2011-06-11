#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for dealing with people's RSVPs."""

import config
config.setup()

from google.appengine.ext import webapp
from aeoid import users as openid_users

import models
import event_lists
from utils.render import render


class ShowResponsePage(webapp.RequestHandler):
    """Showing an RSVP."""
    def get(self, eventid):
        # We use locals() which confuses pylint.
        # pylint: disable-msg=W0612
        ####################################################
        event = models.Event.get_by_id(long(eventid))
        if not event:
            self.redirect('/')
        current_user = openid_users.get_current_user()
        if not current_user:
            self.redirect('/')
            return
        ####################################################

        response, guests = event_lists.get_event_responses(event, current_user)
        self.response.out.write(render(
                'templates/response-show.html', locals()))


class UpdateResponsePage(webapp.RequestHandler):
    """Update an RSVP."""
    def post(self, eventid):
        # We use locals() which confuses pylint.
        # pylint: disable-msg=W0612
        ####################################################
        event = models.Event.get_by_id(long(eventid))
        if not event:
            self.redirect('/')
        current_user = openid_users.get_current_user()
        if not current_user:
            self.redirect('/')
            return
        ####################################################

        response, guests = event_lists.get_event_responses(event, current_user)
        
        # Check if the person is trying to add friends
        try:
            extra_guests = range(
                0, int(self.request.get('friends', '0'))-len(guests))
        except ValueError:
            extra_guests = []

        if extra_guests:
            self.response.out.write(render(
                    'templates/response-friends.html', locals()))
            return
    
        # Remove the current information
        if response is not None:
            response.delete()
        for guest in guests:
            guest.delete()

        response = models.Response(event=event, guest=False)
        response.attending = self.request.get('attending').lower() != 'no'
        response.put()

        guest_names = self.request.get_all('guest_name')
        guest_emails = self.request.get_all('guest_email')
        assert len(guest_names) == len(guest_emails)

        for name, email in zip(guest_names, guest_emails):
            name, email = name.strip(), email.strip()
            if not name or not email:
                continue

            response = models.Response(event=event, guest=True)
            response.attending = True
            response.guest_name = name
            response.guest_email = email
            response.put()

        self.redirect('/event/%s/response/show' % event.key().id())
