#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import config
config.setup()

from google.appengine.api import users as users
from google.appengine.ext.webapp import template

import gravatar

def render(t, kw):
  req = kw['self'].request
  extra = {
      'req': req,
      'config': config,
      'user': users.get_current_user(),
      'login_jsurl': '/login',
      'login_url': users.create_login_url(req.path),
      'logout_url': users.create_logout_url(req.path),
      'appengine_user': users.get_current_user(),
      'appengine_admin': users.is_current_user_admin(),
      'appengine_logout_url': users.create_logout_url(req.path),
      }

  # Don't let people trample on these variables
  common = set(extra.keys()).intersection(kw.keys())
  if common:
    raise SystemError('The following keys are reserved %s' % common)

  kw.update(extra)
  return template.render(t, kw)
  kkk
