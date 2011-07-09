#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Simple pages."""

# Python imports

# Django Imports
from django import shortcuts

# Our App imports


def handler_any(request, template):
    """Handler for any template."""
    return shortcuts.render(request, template+".html")
