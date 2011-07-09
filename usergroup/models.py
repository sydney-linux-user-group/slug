#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module contains the models of objects used in the application."""

#import config
#config.setup()

from django.db import models
from django.contrib.auth.models import User


def get_current_user():
    pass


class Announcement(models.Model):
    """An announcement for an event."""

    def __unicode__(self):
        return u'%s' % self.name

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(
            auto_now_add=True)

    name = models.CharField(max_length=250, blank=False)
    plaintext = models.TextField()
    html = models.TextField()

    published_by = models.ForeignKey(
            User, default=get_current_user, blank=False)
    published_on = models.DateTimeField(
            auto_now_add=True, blank=False)


class Event(models.Model):
    """An event."""

    def get_url(self):
        """Return the canonical url for an event."""
        return "/event/%s" % self.key().id()

    def __unicode__(self):
        return u'%s' % self.name

    created_by = models.ForeignKey(
            User, default=get_current_user, blank=False)
    created_on = models.DateTimeField(
            auto_now_add=True, blank=False)

    name = models.CharField(max_length=250, blank=False)
    input = models.TextField()
    plaintext = models.TextField()
    html = models.TextField()

    published = models.BooleanField(default=False)
    announcement = models.ForeignKey(Announcement)

    emailed = models.BooleanField(default=False)

    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)


class TalkOffer(models.Model):
    """An lightning talk to be given at an event."""

    def get_url(self):
        """Return the canonical url for an event."""
        return "/offer/%s/edit" % self.key().id()

    created_by = models.ForeignKey(
            User, default=get_current_user, blank=False)
    created_on = models.DateTimeField(
            auto_now_add=True, blank=False)

    displayname = models.TextField()
    contactinfo = models.TextField()
    title = models.CharField(max_length=250, blank=False)
    active = models.BooleanField(blank=False,default=True)
    text = models.TextField()
    minutes = models.IntegerField()
    consent = models.BooleanField()


class LightningTalk(models.Model):
    created_by = models.ForeignKey(
            User, default=get_current_user, blank=False)
    created_on = models.DateTimeField(
            auto_now_add=True, blank=False)

    weight = models.IntegerField(default=100, blank=False)
    offer = models.ForeignKey(TalkOffer, blank=False,
            related_name='events')
    event = models.ForeignKey(Event, blank=False,
            related_name='agenda')


class Response(models.Model):
    """An RSVP to attend an event."""
    created_by = models.ForeignKey(
            User, default=get_current_user, blank=False)
    created_on = models.DateTimeField(
            auto_now_add=True, blank=False)

    event = models.ForeignKey(Event, related_name="responses")

    attending = models.BooleanField(blank=False, default=True)

    # Should the response be hidden from everyone?
    #hide = models.BoolenProperty(blank=False, default=False)

    # If this is a guest, then we store their details here, otherwise we just
    # use the creater's details.
    guest = models.BooleanField(blank=False, default=False)
    guest_name = models.TextField()
    guest_email = models.EmailField()
