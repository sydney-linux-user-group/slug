from django.conf.urls.defaults import patterns, url, include

from usergroup.accounts import *

urlpatterns = patterns(
    'usergroup',

    url(r'^accounts/login$', login, name='login'),
    url(r'^accounts/profile$', profile, name='profile'),
    url(r'^accounts/profile/association$', profile, name='profile'),
    url(r'^accounts/profile/disconnected$', profile, name='profile'),
    url(r'^accounts/profile/new$', profile, name='profile'),
    url(r'^accounts/error$', error, name='error'),
    url(r'^accounts/logout$', logout, name='logout'),

    # iCal feeds
    (r'^ical[/]?[^\.]*(?:.ics)?', 'ical.handler', {}),
    (r'^event[/]?[^\.]*(?:.ics)', 'ical.handler', {}),
    (r'^event/ical', 'ical.handler', {}),

    # rss feeds
    (r'^rss', 'rss.handler', {}),
    (r'^\d*/.*feed.*', 'rss.handler', {}),
    (r'^full/.*feed.*', 'rss.handler', {}),
    (r'^event/.*feed.*', 'rss.handler', {}),

    (r'^event/next', 'events.handler_next', {}),

    (r'^event/(.*)/response', 'response.handler', {}),
    (r'^event/(.*)/response', 'response.handler', {}),

    (r'^event/(.*)/publish', 'event_publish.handler', {}),
    (r'^event/(.*)/email', 'event_publish.handler_email', {}),

    (r'^event/(add)', 'event_edit.handler', {}),
    (r'^event/(.*)/edit', 'event_edit.handler', {}),

    (r'^event/(.*)/addoffer', 'event_edit.handler_offer_add', {}),
    (r'^event/(.*)/remoffer', 'event_edit.handler_offer_remove', {}),
    (r'^event/(.*)', 'events.handler_event', {}),

    (r'^events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?',
         'events.handler_events', {}),

    (r'^event', 'events.handler_event', {}),

    (r'^offer/(.*)', 'offer_edit.handler', {}),
    (r'^offers', 'offers.handler', {}),

    (r'^(?P<template>.+)', 'utils.handler_any', {}),

    (r'^$', 'events.handler_events', {
        'template': 'index.html', 'published_default': True}),
)
