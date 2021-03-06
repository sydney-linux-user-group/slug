``README`` - Overview for developers
====================================

More documentation
------------------

We're starting to add more documentation into the ``doc`` folder.

If you would prefer to read formatted HTML (highly recommended),
simply ``make doc`` and then look under ``doc/_build/html``

This ``README`` is automatically generated and placed at the top level as part
of that documentation build. If you're editing this at the top level, your
changes will shortly be clobbered. Edit ``doc/README.rst`` instead.

You can browse the latest checked-in version of the docs at http://slug-usergroup.rtfd.org

You can check the status of the latest checking thanks to our free CI service from `Travis`_

.. _Travis: http://travis-ci.org/#!/sydney-linux-user-group/slug

Initial Configuration
---------------------

To get the code and dependencies::

   git clone git@github.com:sydney-linux-user-group/slug.git
   cd slug
   make install

Running a test server
---------------------

Simply ``make serve``; this will configure a virtualenv, download and install
dependencies (inside the virtualenv; your system will not be touched); and a
test server will be started.

If this is your first time running ``make serve`` you'll be prompted to provide
a username and password for an admin account.

Running tests
-------------

Simply ``make test``

Coding standards
----------------

In general, we follow PEP-8_. ``make lint`` will tell you in detail about all the
things we need to fix.

.. _PEP-8: http://www.python.org/dev/peps/pep-0008/


Production Deployment
---------------------

#. To account for differences between the dev and prod infrastructure, we have
   a ``private`` repo which needs to be checked out. Exactly where the
   ``private`` repo comes from will be specific to your deployment.

   To see where this is used and get an idea of what you can override, search
   for ``private`` in settings.py

   .. highlight:: console

#. The SLUG deployment uses one user to deploy the code, and another user to
   run the code::

      zhasper@tridge:~$ grep slug /etc/passwd /etc/group
      /etc/passwd:slug:x:1001:1001::/home/slug:/bin/bash
      /etc/passwd:slug-run:x:1005:1005::/home/slug-run:/bin/sh
      /etc/group:slug:x:1001:
      /etc/group:slug-run:x:1005:slug

#. Usually, the run user should only need read access to the files you've
   checked out. If there are specific files or directories that the run user
   needs to write to [1]_, simply use ``chgrp slug-run $FILE; chmod g+w $FILE``
   to make them accessible to both the deploy and run users. If this needs to
   be persisted across deployments, you may have to take care of this in your
   deploy script.

#. For deployment, I simply ``ssh slug@localhost -A``; this turns on agent
   forwarding so that my usual SSH keys are used to pull the code from
   bitbucket. For automated deployments, you can create a passwordless key
   stored for the ``slug`` user to use and upload it to Github as a `deploy
   key`_

   .. _deploy key: http://help.github.com/deploy-keys/

   .. highlight:: bash

#. To do the deployment, I use this simple script, which would benefit from a ton more checking::

      #!/bin/bash

      TIMESTAMP=$(date +%Y%m%d-%H%M)
      cd ~/django
      git clone -b django git@github.com:sydney-linux-user-group/slug.git ${TIMESTAMP}
      cd ${TIMESTAMP}
      make install
      make private
      make prepare-serve

   This makes it relatively easy to revert to an earlier version of the code.

   .. note::

      Depending on your database setup you may have to do some extra work here.
      If using sqlite you will want to point the new checkout at your existing
      sqlite database somewhow. If you're using ``mysql`` or ``postgres``
      (configured in ``private/settings.py``) you'll probably want to take a
      backup of the existing database before running ``make prepare-serve`` in
      case you need to roll back the database changes.

      .. highlight:: console

#. We've chosen to run the app inside `Green Unicorn`_, and have it started by
   ``upstart``::

      slug@tridge:~/django/current$ cat /etc/init/slug.conf 
      description "SLUG Django instance"
      start on runlevel [2345]
      stop on runlevel [06]
      respawn
      respawn limit 10 5
      script
        cd /home/slug/django/current
        bin/gunicorn_django -u slug-run -g slug-run
      end script
      slug@tridge:~/django/current$ ls -l /etc/init.d/ | grep slug
      lrwxrwxrwx 1 root root    21 2012-02-04 23:24 slug -> /lib/init/upstart-job

   This solution is not perfect. ``upstart`` doesn't kill ``gunicorn``
   properly, so a restart involves killing a few processes before using ``sudo
   service slug start``. I need to find time to figure out how to improve this.

   .. _Green Unicorn: http://gunicorn.org/

   .. highlight:: nginx

#. We've chosen to use `nginx`_ as a frontend, and to serve static files. Only
   a few changes from the default config are needed to accomplish this::

      # path for static files
      root /home/slug/django/current/usergroup/;

      location /static/ {
              alias /tmp/slug-static/;
      }

      location /admin/media/ {
              root /home/slug/django/current/lib/python2.6/site-packages/django/contrib;
      }

      location / {
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header Host $http_host;
          proxy_redirect off;

          proxy_pass   http://localhost:8000/;

   ``/tmp/slug-static`` is stipulated as the STATIC_ROOT in ``settings.py``. We
   should really get around to fixing this - it just needs to be a location
   that the deploy user can write to and the user running nginx can read from.

   .. _nginx: http://nginx.org/en/

.. rubric:: Footnotes

.. [1] For instance, if you're using ``sqlite`` as the database, the run
       user will need permission to write to the ``sqlite`` file

..  vim: set ts=2 sw=2 tw=0 et:
