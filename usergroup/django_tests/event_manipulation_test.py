#!/usr/bin/env python
"""Tests around creating, publishing, and announcing meetings.

Does not use selenium, so cannot test client behaviour."""

import datetime
import random

import django.test
import django.core.mail

import usergroup.event_edit

#TestCases have lots of public methods
#pylint: disable=R0904
#Yes, method names are long.
#pylint: disable=C0103
#Really no point creating docstrings for most of this
#pylint: disable=C0111

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

class TestPublishSomeEvents(django.test.TestCase):
    """Test that only published events show as being published."""

    fixtures = ['test_admin_user', 'two_unpublished_events']

    def test_unpublished_events_show_as_unpublished(self):
        """Test that only published events show as being published."""
        self.client.login(username="admin", password="admin")
        response = self.client.get('/events')
        #Two events, ready to publish
        self.assertContains(response, '<input id="submit_1" type="submit" '
                            'value="Publish event">')
        self.assertContains(response, '<input id="submit_2" type="submit" '
                            'value="Publish event">')
        #Publish the first event
        response = self.client.post('/event/1/publish', follow=True)
        #First event should now be ready for announcement
        self.assertContains(response, '<input id="submit_1" type="submit" '
                            'value="Announce event via email">')
        #Second event should still be waiting to be published
        self.assertContains(response, '<input id="submit_2" type="submit" '
                            'value="Publish event">')

class TestEventVisibility(django.test.TestCase):
    """Test that unpublished events cannot be seen except by admins."""

    fixtures = ['test_admin_user', 'test_existing_user',
                'two_unpublished_events']

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.client.post('/event/1/publish', follow=True)
        self.client.logout()

    def test_visibility_as_anonymous_user(self):
        response = self.client.get('/events')
        #Two events, ready to publish
        self.assertContains(response, '<a class=eventname href="/event/1">'
                            'Monthly Meeting</a>')
        self.assertNotContains(response, '<a class=eventname href="/event/2">'
                               'asfdadsf</a>')

    def testVisibilityAsOrdinaryUser(self):
        self.client.login(username='existing', password='password')
        response = self.client.get('/events')
        #Two events, ready to publish
        self.assertContains(response, '<a class=eventname href="/event/1">'
                            'Monthly Meeting</a>')
        self.assertNotContains(response, '<a class=eventname href="/event/2">'
                               'asfdadsf</a>')
        self.client.logout()

class TestEventEmail(django.test.TestCase):
    """Test the emails that get sent out when an event is announced."""

    fixtures = ['test_admin_user', 'two_unpublished_events']

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.client.post('/event/1/publish', follow=True)
        self.client.post('/event/1/email', follow=True)

    def test_one_email_sent(self):
        self.assertEqual(len(django.core.mail.outbox), 1)

    def test_email_from(self):
        self.assertEqual(django.core.mail.outbox[0].from_email,
                         "committee@slug.org.au")

    def test_email_to(self):
        self.assertEqual(django.core.mail.outbox[0].to,
                         ["announce@slug.org.au"])

    def test_subject(self):
        self.assertEqual(django.core.mail.outbox[0].subject, "Monthly Meeting")

    def test_update_email_sent(self):
        self.client.post('/event/1/email', follow=True)
        self.assertEqual(len(django.core.mail.outbox), 2)

    def test_update_email_subject(self):
        self.client.post('/event/1/email', follow=True)
        self.assertEqual(django.core.mail.outbox[1].subject,
                         "Updated: Monthly Meeting")

    def test_message_body_has_no_template_tags(self):
        body = django.core.mail.outbox[0].body
        self.assertNotIn('{{', body)
        self.assertNotIn('{%', body)

    def test_title_in_message_body(self):
        body = django.core.mail.outbox[0].body
        self.assertIn('====== March 2012 SLUG Meeting ======', body)

    def test_date_in_body(self):
        body = django.core.mail.outbox[0].body
        self.assertIn('Date: Friday, March 30, 2012', body)

    def test_start_time_in_body(self):
        body = django.core.mail.outbox[0].body
        self.assertIn('* Start: Arrive at 6pm for a 6:30pm start', body)

class TestEventEditing(django.test.TestCase):
    """Ensure that editing an event propagates changes."""

    fixtures = ['test_admin_user', 'single_unpublished_event']

    def setUp(self):
        self.client.login(username="admin", password="admin")
        self.client.post('/event/1/publish', follow=True)
        self.client.post('/event/1/email', follow=True)
        self.request_data = {'start': 'March 30, 2012, 6 p.m.',
                             'end': 'March 30, 2012, 8 p.m.',
                             'input': '{{event.name}}',
                             'name': 'Sample Meeting'}

    def test_edit_event_name(self):
        self.request_data['name'] = 'Weekly Meeting'
        response = self.client.post('/event/1', data=self.request_data,
                                    follow=True)
        self.assertContains(response, 'name="name" value="Weekly Meeting"')

    def test_plaintext_contains_new_event_name(self):
        self.request_data['name'] = 'Plaintext Meeting'
        response = self.client.post('/event/1', data=self.request_data,
                                    follow=True)
        self.assertContains(
                response, '<pre class="eventOutput">Plaintext Meeting</pre>')

    def test_html_contains_new_event_name(self):
        self.request_data['name'] = 'HTML Meeting'
        response = self.client.post('/event/1', data=self.request_data,
                                    follow=True)
        self.assertContains(
                response, '<p>HTML Meeting</p>')

    def test_email_contains_new_event_name(self):
        self.request_data['name'] = 'Email Meeting'
        self.client.post('/event/1', data=self.request_data,
                                    follow=True)
        _ = self.client.post('/event/1/publish', follow=True)
        self.client.post('/event/1/email', follow=True)
        body = django.core.mail.outbox[1].body
        self.assertIn('Email Meeting', body)

    def test_event_ready_for_republish(self):
        self.buffer = True
        response = self.client.get('/events')
        self.assertContains(
                response, '<div class=publishform id="publish_1">\n'
                '                 <!-- No change -->')
        self.request_data['name'] = 'Republished Meeting'
        self.client.post('/event/1', data=self.request_data)
        response = self.client.get('/events')
        self.assertContains(
                response, '<!-- Event was published, then changed"-->\n'
                '                <input id="submit_1"')
