#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""
Fix the error messages when running tests.
"""

from django.core.handlers.base import BaseHandler


def _handle_uncaught_exception(self, request, resolver, exc_info):
    """
    Processing for any otherwise uncaught exceptions (those that will
    generate HTTP 500 responses). Can be overridden by subclasses who want
    customised 500 handling.

    Be *very* careful when overriding this because the error could be
    caused by anything, so assuming something like the database is always
    available would be an error.
    """
    from django.conf import settings
    from django.core.mail.message import EmailMessage
    from django.views import debug

    if settings.DEBUG_PROPAGATE_EXCEPTIONS:
        raise

    technical_500_response = debug.technical_500_response(request, *exc_info)
    return technical_500_response

BaseHandler.handle_uncaught_exception = _handle_uncaught_exception
