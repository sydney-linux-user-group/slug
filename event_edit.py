#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Module for creating and editing Event objects."""

import config
config.setup()

# Python Imports
import os
import os.path
import simplejson
import traceback
import cStringIO as StringIO
from datetime import datetime

# AppEngine Imports
from google.appengine.ext import webapp
from django import template

# Third Party imports
from dateutil import rrule
from datetime_tz import datetime_tz
import markdown
import logging

# Our App imports
import models
import offers
from utils.render import render as r


# We don't want to wrap this line as we use a grep to extract the details
# pylint: disable-msg=C0301
extensions = ['abbr', 'footnotes', 'def_list', 'fenced_code', 'tables', 'subscript', 'superscript', 'slugheader', 'anyurl']


def lastfridays():
    """Return 5 last Fridays of the month."""
    return list(x.date() for x in rrule.rrule(
         rrule.MONTHLY, interval=1, count=10, byweekday=(rrule.FR(-1)),
         dtstart=datetime.now()))


def get_templates():
    """Get all the markdown templates."""
    ret = []

    directory = "templates/markdown"
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue

        fullpath = os.path.join(directory, filename)
        name = filename.replace('.md', '')
        ret.append((name, file(fullpath).read()))
    return ret


class AddOffer(webapp.RequestHandler):
    """Adds an offer to an event"""

    def post(self, key):
        if not key:
            self.redirect('/events')
            return
        event = models.Event.get(key)
        offerkey = self.request.get('id')
        offer = models.TalkOffer.get(offerkey)

        talk = models.LightningTalk(event=event, offer=offer)
        talk.put()

        self.response.headers['Content-Type'] = 'application/javascript'
        output = simplejson.dumps({'key': str(talk.key())})
        logging.debug('output: %s', output)
        self.response.out.write(output);

class RemOffer(webapp.RequestHandler):
    """Removes an offer from an event."""

    def post(self, key):
        if not key:
            self.redirect('/events')
            return
        talkkey = self.request.get('id')
        talk = models.LightningTalk.get(talkkey)
        talk.delete()
        self.response.headers['Content-Type'] = 'application/javascript'
        output = simplejson.dumps({'deleted': str(True)})



class EditEvent(webapp.RequestHandler):
    """Handler for creating and editing Event objects."""

    def get(self, key=None):
        # We use locals() which confuses pylint.
        # pylint: disable-msg=W0612
        if key:
            try:
                key = long(key)
                event = models.Event.get_by_id(key)
                assert event
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/events')
                return
        else:
            event = None

        template_values = {}

        if event:
            template_values['agenda'] = offers.get_event_agenda(event)
        else:
            template_values['agenda'] = None

        template_values['event'] = event
        template_values['fridays'] = lastfridays()
        template_values['templates'] = get_templates()
        template_values['self'] = self
        template_values['offers'] = models.TalkOffer.all().fetch(limit=100)

        self.response.out.write(r(
            'templates/editevent.html', template_values
            ))

    def post(self, key=None):
        event_name = self.request.get('name')
        if key:
            try:
                key = long(key)
                event = models.Event.get_by_id(key)
                event.name = event_name
            # pylint: disable-msg=W0702
            except (AssertionError, ValueError):
                self.redirect('/events')
                return
        else:
            #name is a required field; must populate now. Rest comes later.
            event = models.Event(name=event_name, text='', html='',
                    start=datetime.now(), end=datetime.now())

        inputtext = self.request.get('input')

        start_date = self.request.get('start')
        end_date = self.request.get('end')
        if start_date.starts_with('Sept.'):
            start_date = start_date.replace('Sept.', 'Sep.')
        if end_date.ends_with('Sept.'):
            end_date = end_date.replace('Sept.', 'Sep.')


        start_date = datetime_tz.smartparse(start_date)
        end_date = datetime_tz.smartparse(end_date)

        event.input = inputtext
        event.start = start_date.asdatetime()
        event.end = end_date.asdatetime()

        event.put()

        # We can't do this template subsitution until we have saved the event.
        try:
            plaintext = str(template.Template(inputtext).render(
                            template.Context({
                                'event': event,
                                'req': self.request,
                                'agenda': offers.get_event_agenda(event)
                            }), ))
            html = markdown.markdown(plaintext, extensions).encode('utf-8')
            event.plaintext = plaintext
            event.html = html
        except Exception:
            sio = StringIO.StringIO()
            traceback.print_exc(file=sio)
            event.plaintext = sio.getvalue()

        logging.debug("e.a %s, e.n %s", event.announcement, event.name)

        event.put()

        self.redirect('%s/edit' % event.get_url())
