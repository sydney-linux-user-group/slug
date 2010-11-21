

from google.appengine.ext.webapp import template
import aeoid.users as openid_users

import gravatar

def render(t, kw):
  extra = {
      'openid_user': openid_users.get_current_user(),
      'login_url': openid_users.create_login_url('/'),
      'logout_url': openid_users.create_logout_url('/'),
      }

  # Check people havn't accidently log
  common = set(extra.keys()).intersection(kw.keys())
  if common:
    raise SystemError('The following keys are reserved %s' % common)

  kw.update(extra)
  return template.render(t, kw)
