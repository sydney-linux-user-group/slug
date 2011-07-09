from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'usergroup',

    # iCal feeds
    (r'/ical[/]?[^\.]*(?:.ics)?', 'ical.handler', {}),
    (r'/event[/]?[^\.]*(?:.ics)', 'ical.handler', {}),
    (r'/event/ical', 'ical.handler', {}),

    # rss feeds
    (r'/rss', 'rss.handler', {}),
    (r'/\d*/.*feed.*', 'rss.handler', {}),
    (r'/full/.*feed.*', 'rss.handler', {}),
    (r'/event/.*feed.*', 'rss.handler', {}),

    (r'/event/next', 'events.handler_next', {}),
    (r'/event/(.*)/response', 'response.handler', {}),
    (r'/event/(.*)/response', 'response.handler', {}),

    (r'/event/(.*)/publish', 'event_publish.handler', {}),
    (r'/event/(.*)/email', 'event_publish.handler_email', {}),

    (r'/event/(.*)/edit', 'event_edit.handler', {}),
    (r'/event/(.*)/addoffer', 'event_edit.handler_offer_add', {}),
    (r'/event/(.*)/remoffer', 'event_edit.handler_offer_remove', {}),
    (r'/event/(.*)', 'events.handler_event', {}),

    (r'/events[/]?(?P<year>[^/]*)[/]?(?P<month>[^/]*)[/]?(?P<day>[^/]*)[/]?',
         'events.handler_events', {}),
    (r'/events.*', 'events.handler_events', {}),

    (r'/offer/(.*)', 'offer_edit.handle', {}),
    (r'/offer/add', 'offer_edit.handle', {}),
    (r'/offers', 'offers.handle', {}),

    (r'/(?P<template>.*)', 'django.shortcuts.render', {}),

    (r'', 'events.handler_events', {
        'template': 'index.html', 'published_default': True}),

)
