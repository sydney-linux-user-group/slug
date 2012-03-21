#!/usr/bin/env python
"""Tests around creating, publishing, and announcing meetings.

Does not use selenium, so cannot test client behaviour."""

import datetime
import random

import django.test

import usergroup.event_edit

#TestCases have lots of public methods
#pylint: disable=R0904

class TestCreateEvent(django.test.TestCase):
    """Test simple event creation."""

    fixtures = [ 'test_admin_user' ]

    def test_create_event(self):
        """Hitlist: Create an event."""
        self.client.login(username='admin', password='admin')

        fridays = usergroup.event_edit.lastfridays()
        friday = random.choice(fridays)
        start, end = usergroup.event_edit.meeting_times(friday)

        meeting_details = {'start': start, 'end': end, 'name': 'NameyName',
                           'input': 'MeetingDetails'}
        response = self.client.post(
                '/event/None', meeting_details, follow=True)
        final_url = response.redirect_chain[-1][0]
        self.assertEqual('http://testserver/event/1/edit', final_url)
        self.assertContains(response, 'name="name" value="NameyName"') 

class TestEditEvent(django.test.TestCase):
    """Test methods from edit_event."""

    def test_meeting_times(self):
        """Test that feeding a date returns expected timestamps."""
        meeting_date = datetime.date(2012, 3, 30)
        start, end = usergroup.event_edit.meeting_times(meeting_date)
        self.assertEqual("March 30, 2012 06:30PM", start)
        self.assertEqual("March 30, 2012 08:00PM", end)


class TestPublishEvent(django.test.TestCase):
    """Test things that happen when publishing events."""

    fixtures = ['test_admin_user', 'single_unpublished_event']

    def test_ready_to_publish(self):
        """Test that a newly created event shows as ready to publish."""
        self.client.login(username="admin", password="admin")
        response = self.client.get('/events')
        self.assertContains(response, '<input id="submit_1" type="submit" '
                            'value="Publish event">')
