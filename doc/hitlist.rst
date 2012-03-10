``Hitlist`` - Things we need to test
====================================

Validate event creation
-----------------------

  * Login as an administrator
  * Click "add event"
  * Choose a date and template
  * Add a title
  * Submit
  * Navigate to the events page
  * Verify that the event shows as being unpublished

Status: Implemented.

  .. automethod:: usergroup.selenium_tests.create_and_manipulate_meetings_test.TestEventCreationAndPublication.testCreateEvent


Validate event publication
--------------------------

  * Install a fixture with two unpublished events
  * Load the events page as an admin
  * Publish one event
  * Verify that events page shows that event as being published
  * Verify that events page does not show the other event as being published

Normal users cannot see unpublished events
------------------------------------------

  * Install a fixture with at least one published and one unpublished event
  * Load the front page as a normal user
  * Verify that all published events are visible
  * Verify that all unpublished events are not visible

Anonymous users cannot see unpublished events
---------------------------------------------

  * Install a fixture with at least one published and one unpublished event
  * Load the front page as a an anonymous
  * Verify that all published events are visible
  * Verify that all unpublished events are not visible

Announce an event
-----------------

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
-----------------------

  * Install a fixture with at least one 1 published announced event
  * Load the event detail page as an admin
  * Edit the details of the event and submit changes
  * Load the event list page as an admin
  * Verify that the event now shows ready to be re-published

Re-publish an event
-------------------

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
--------------------------------

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
