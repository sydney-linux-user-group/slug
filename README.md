# Initial Configuration

To get the code and dependencies:

> git clone https://github.com/sydney-linux-user-group/slug.git
> cd slug
> make third_party

# Installing django 1.2.5

We use django1.2.5, which is bundled with the SDK.

You don't gots to do nothing.

# Running appserver on a mac

We need to use python2.6, not python2.7. ``make serve`` will start the dev appserver using python2.6 for you.

# Adding third-party libraries

- First, edit ``third_party/Makefile`` to tell Make how to download the dependency (and how to tell if it's already downloaded). We have existing examples that fetch tarfiles and svn checkouts.
- Then, edit ``third_party.paths`` to list the directorys/files to add to sys.path/the third_party.zip file.
- Finally, a "make third_party" should rebuild the zipfile for you. You don't need to do this manually - "make serve" or "make deploy" will rebuild this if needed.

# Pushing to appengine

 - If neccessary, increment version number in app.cfg to make sure you don't trample on the currently-live version of the app
 - run ``make deploy`` to push to server
