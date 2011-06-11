#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:
#
# pylint: disable-msg=C0111
"""
Configuration file for Python AppEngine runtime.

Our current settings are:
 * Forces everything to use Django 1.2
 * Adds appstats.
"""
webapp_django_version = "1.2"

def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app
