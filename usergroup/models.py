#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module contains the models of objects used in the application."""

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    """An announcement for an event."""

    def __unicode__(self):
        return u'%s' % self.name

    created_by = models.ForeignKey(User, blank=False, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=250, blank=False)
    plaintext = models.TextField()
    html = models.TextField()

    published_by = models.ForeignKey(
            User, blank=False, related_name='+')
    published_on = models.DateTimeField(
            auto_now_add=True, blank=False)

class AnnouncementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Announcement, AnnouncementAdmin)


class Event(models.Model):
    """An event."""

    def get_url(self):
        """Return the canonical url for an event."""
        return "/event/%s" % self.pk

    def __unicode__(self):
        return u'%s' % self.name

    created_by = models.ForeignKey(User, blank=False, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=250, blank=False)
    input = models.TextField()
    plaintext = models.TextField()
    html = models.TextField()

    published = models.BooleanField(default=False)
    announcement = models.ForeignKey(Announcement, null=True)

    emailed = models.BooleanField(default=False)

    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)

class EventAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventAdmin)


class TalkOffer(models.Model):
    """An lightning talk to be given at an event."""

    def get_url(self):
        """Return the canonical url for an event."""
        return "/offer/%s/edit" % self.pk

    created_by = models.ForeignKey(User, blank=False, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)

    displayname = models.TextField()
    contactinfo = models.TextField()
    title = models.CharField(max_length=250, blank=False)
    active = models.BooleanField(blank=False,default=True)
    text = models.TextField()
    minutes = models.IntegerField()
    consent = models.BooleanField()

class TalkOfferAdmin(admin.ModelAdmin):
    pass
admin.site.register(TalkOffer, TalkOfferAdmin)


class LightningTalk(models.Model):
    created_by = models.ForeignKey(User, blank=False, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)

    weight = models.IntegerField(default=100, blank=False)
    offer = models.ForeignKey(TalkOffer, blank=False,
            related_name='events')
    event = models.ForeignKey(Event, blank=False,
            related_name='agenda')

class LightningTalkAdmin(admin.ModelAdmin):
    pass
admin.site.register(LightningTalk, LightningTalkAdmin)


class Response(models.Model):
    """An RSVP to attend an event."""
    created_by = models.ForeignKey(User, blank=False, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)

    event = models.ForeignKey(Event, related_name="responses")

    attending = models.BooleanField(blank=False, default=True)

    # Should the response be hidden from everyone?
    #hide = models.BoolenProperty(blank=False, default=False)

    # If this is a guest, then we store their details here, otherwise we just
    # use the creater's details.
    guest = models.BooleanField(blank=False, default=False)
    guest_name = models.TextField()
    guest_email = models.EmailField()

class ResponseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Response, ResponseAdmin)
