Tests -- How we know that stuff ain't done broke.
-------------------------------------------------

Selenium tests -- Test client-side behaviour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`base` - Base classes and common code for selenium tests
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. tip:: While it's very cool, testing with Selenium is slow due to the need to
    fire up a Firefox process and wait for page rendering. Selenium should only be
    used when testing client-side behaviours.

.. warning:: If your computer doesn't have a working internet connection,
    Firefox will switch to offline mode and not even try connecting to localhost.
    This breaks the tests. Good job, Firefox!

.. automodule:: usergroup.selenium_tests.base
  :members:
  :undoc-members:
  :show-inheritance:

:mod:`create_and_manipulate_meetings_test`
""""""""""""""""""""""""""""""""""""""""""

.. automodule:: usergroup.selenium_tests.create_and_manipulate_meetings_test
  :members:
  :undoc-members:
  :show-inheritance:

:mod:`login_test` - Walking through the login process
"""""""""""""""""""""""""""""""""""""""""""""""""""""

.. automodule:: usergroup.selenium_tests.login_test
  :members:
  :undoc-members:
  :show-inheritance:

:mod:`register_and_respond_test` - New user registration and handling
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. automodule:: usergroup.selenium_tests.register_and_respond_test
  :members:
  :undoc-members:
  :show-inheritance:

Django tests -- Test views and backend functionality only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`email_test` -- Test that emails get sent appropriately
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. note:: Currently very incomplete

.. automodule:: usergroup.django_tests.email_test
  :members:
  :undoc-members:
  :show-inheritance:

:mod:`login_test` -- Test that logins work as expected
""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. automodule:: usergroup.django_tests.login_test
  :members:
  :undoc-members:
  :show-inheritance:
