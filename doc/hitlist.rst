``Hitlist`` - Things we need to test
====================================

Event creation and publication
------------------------------

Create an event
^^^^^^^^^^^^^^^

* Fixtures:

  * Single admin user

* Login as an administrator
* Click "add event"
* Choose a date and template
* Add a title
* Submit
* Verify that we've been redirected appropriately.

Implemented in :func:`usergroup.django_tests.event_manipulation_test.TestCreateEvent.test_create_event`

Newly created events are ready to publish
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Fixtures:

  * Single admin user
  * One unpublished event

* As an admin, browse to the Events List page
* Find the submit button associated with the event
* Verify that the button says "Publish Event"

Implemented in :func:`usergroup.django_tests.event_manipulation_test.TestPublishEvent.test_ready_to_publish`

Publish an event
^^^^^^^^^^^^^^^^

* Fixtures:

  * Two unpublished events
  * One admin user

* Install a fixture with two unpublished events
* Load the events page as an admin
* Publish one event
* Verify that events page shows that event as being published (ie, ready to announce)
* Verify that events page does not show the other event as being published

Implemented in :func:`usergroup.django_tests.event_manipulation_test.TestPublishSomeEvents.test_unpublished_events_show_as_unpublished`

Normal users cannot see unpublished events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one published and one unpublished event
* Load the front page as a normal user
* Verify that all published events are visible
* Verify that all unpublished events are not visible

Implemented in :func:`usergroup.django_tests.event_manipulation_test.TestEventVisibility.testVisibilityAsOrdinaryUser`

Anonymous users cannot see unpublished events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one published and one unpublished event
* Load the front page as a an anonymous
* Verify that all published events are visible
* Verify that all unpublished events are not visible


Implemented in :func:`usergroup.django_tests.event_manipulation_test.TestEventVisibility.testVisibilityAsAnonymousUser`

Announce an event
^^^^^^^^^^^^^^^^^

* Install a fixture with at least 1 published unannounced event
* Load the events page as an admin
* Verify that the event shows as being unannouned
* Announce the event
* Verify that the event shows as having been announced
* Django outbox should contain one email

  * Validate from address
  * Validate to address
  * Check that body has nothing that looks like a template tag
  * Check that tile is present in body
  * Check that date and time are in body

Edit an announced event
^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one 1 published announced event
* Load the event detail page as an admin
* Edit the details of the event and submit changes
* Load the event list page as an admin
* Verify that the event now shows ready to be re-published

Re-publish an event
^^^^^^^^^^^^^^^^^^^

* Install a fixture with one published announced edited event ready for re-publication
* Load the event list page as an admin
* Verify that the event shows as being ready for re-publication

* Load the event list as an anonymous user
* Verify that the event list shows the old issue details

* Republish the event
* Load the event list page as an admin
* Verify that the event list page shows the event being ready for re-announcement

* Load the event list as an anonymous user
* Verify that the event list shows the new issue details

Re-announce a re-published event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with one published announced edited re-published event ready for re-announcement
* Load the event list page as an admin
* Verify that the list shows the event as ready for re-announcement
* Re-announce the event
* Verify that the event list page shows as having been re-announced
* Django outbox should contain one email

  * Validate from address
  * Validate to address
  * Check that body has nothing that looks like a template tag
  * Check that tile is present in body
  * Check that date and time are in body
  * Validate that the subject indicates that this is a re-announcement

Create and edit talk offers
---------------------------

Anonymous user clicks "offers a talk"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Browse the main page as an anonymous user
* Click "Offer Talk"
* Get redirected to the login page

Logged-in user offers a talk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Browse the main page as a logged-in user
* Click "Offer Talk"
* A second window opens with the "Offer Talk" form
* Enter values into all fields
* Submit the form
* Verify that the window has redirected to "/offer/add#prevoffers"
* Verify that the entered talk details show in the list of previous offers

Admin looks at list of talk offers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one offered talk
* As an admin, browse the list of offers
* Verify that the offered talks are listed

Admin edits agenda for a meeting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture containing at least one offered talk and one published event
* As an admin, load the detail page for an event
* Click on the "Agenda" tab
* Drag a talk from "All Offers" to "Agenda Items"
* Verify that the talk was dropped into Agenda Items; and has turned orange
* Click on the Source tab and submit the form
* Click on "Formatted Plaintext" and "HTML" and verify that the talk is shown in the agenda






