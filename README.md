# Initial Configuration

To get the code and dependencies::

  git clone git@github.com:mithro/slug.git
  cd slug
  ./init_third_party.sh

# Installing django 1.2.5

We use django1.2.5, which is bundled with the SDK.

You don't gots to do nothing.

# Running appserver on a mac

We need to use python2.6, not python2.7.

You'll need to use::

   /usr/bin/python2.6 /usr/local/bin/dev_appserver.py .

to start the appserver.

# Adding third-party libraries

 - Edit the init-third-party script to download and unpack your library
 - edit third-party/mkzip to include the neccessary portions of the unpacked library in the zip
 - run third-party/mkzip
 - edit config.py to include the library in the sys.path

# Pushing to appengine

 - If neccessary, increment version number in app.cfg to make sure you don't trample on the currently-live version of the app
 - run ``appcfg.py update .`` to push to server
