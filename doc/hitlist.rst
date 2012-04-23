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

.. py:currentmodule:: usergroup.django_tests.event_manipulation_test

Implemented in :func:`TestCreateEvent.test_create_event`

Newly created events are ready to publish
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Fixtures:

  * Single admin user
  * One unpublished event

* As an admin, browse to the Events List page
* Find the submit button associated with the event
* Verify that the button says "Publish Event"

Implemented in :func:`TestPublishEvent.test_ready_to_publish`

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

Implemented in :func:`TestPublishSomeEvents.test_unpublished_events_show_as_unpublished`

Normal users cannot see unpublished events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one published and one unpublished event
* Load the front page as a normal user
* Verify that all published events are visible
* Verify that all unpublished events are not visible

Implemented in :func:`TestEventVisibility.testVisibilityAsOrdinaryUser`

Anonymous users cannot see unpublished events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one published and one unpublished event
* Load the front page as a an anonymous
* Verify that all published events are visible
* Verify that all unpublished events are not visible


Implemented in :func:`TestEventVisibility.testVisibilityAsAnonymousUser`

Announce an event
^^^^^^^^^^^^^^^^^

* Install a fixture with at least 1 published unannounced event
* Announce the event
* Django outbox should contain one email

  * Validate from address
  * Validate to address
  * Check that the subject is the meeting name
  * Check that if the meeting is re-announced, the second email has "Updated: "
    plus the meeting name.
  * Check that body has nothing that looks like a template tag
  * Check that title is present in body
  * Check that date and time are in body

Implemented in :class:`TestEventEmail`

Edit an announced event
^^^^^^^^^^^^^^^^^^^^^^^

* Install a fixture with at least one 1 published announced event
* Load the event detail page as an admin
* Edit the details of the event and submit changes
* Load the event list page as an admin. Verify that the event now shows ready
  to be re-published
* Load the event details page as an admin. Verify that the HTML and Plaintext
  views ahve been updated.
* Re-publish the event, and verify that the updated information is used to
  generate the email.

Implemented in :class:`TestEventEditing`

Re-publish an event
^^^^^^^^^^^^^^^^^^^

* Install a fixture with one published announced edited event ready for re-publication
* Load the event list page as an admin
* Verify that the event shows as being ready for re-publication
* Implemeneted in :func:`TestEventEditing.test_event_ready_for_republish`

* Load the event list as an anonymous user
* Verify that the event list shows the old issue details
* Done in :func:`TestEventEditing.test_event_shows_old_details_for_anonymous_user`

* Republish the event
* Load the event list page as an admin
* Verify that the event list page shows the event being ready for re-announcement
* Done in :func:`TestEventEditing.test_republished_event_shows_as_ready_for_reannouncement`

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


Normal user interaction
------------------------------

Assume starts with "Able to"


Login with username/password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Admin user can login with username/password
* Valid existing user can login with username/password
* Invalid user can't login username/password

Login with OpenID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Admin user can login
* Valid existing user can login
* Invalid OpenID goes to Create a new account option below.

Implemented in :class:`TestValidAdminLogin`
Implemented in :class:`TestInvalidUserLogin`
Implemented in :class:`TestValidNonAdminLogin`


Create a new account using OpenID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Including checking of the email address from non-trusted providers.


Create a new account using username/password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Including checking of the email address.

* testFailOnMissingField
* testFailOnNonMatchingPasswords
* testFailOnInvalidEmailAddress
* testFailOnExistingUsername
* testFailOnExistingEmail
* testRegistrationSuccess

Implemented in :class:`TestRegister`


Change/add local password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Add an OpenID account to an existing account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Remove an OpenID account to an existing account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Merge two accounts (OpenID/OpenID, OpenID/login)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Say Yes to attending an event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Say No to attending an event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Bring friends to attending an event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


get to via links
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* map
* webirc on freenode
* mailing list
* calendar


--------------------------------------------------------

"quick tweet" about attending an event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"quick facebook post" about attending an event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

to sign up to the mailing list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^






