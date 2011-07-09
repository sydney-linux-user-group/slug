# Based on example code from:
#   http://en.gravatar.com/site/implement/images/python/

import urllib, hashlib

from django.template.defaultfilters import stringfilter, register

@register.filter
@stringfilter
def gravatar(email, size=40, rating='pg'):
  if size <= 32:
    default = "http://%s/images/silhouette-small.png" % settings.HOST
  else:
    default = "http://%s/images/silhouette.png" % settings.HOST

  # construct the url
  gravatar_url = "http://www.gravatar.com/avatar/"
  gravatar_url += hashlib.md5(email.lower().strip()).hexdigest()
  gravatar_url += "?"
  gravatar_url += urllib.urlencode({
      'd':default, 's':str(size), 'r':rating})
  return gravatar_url
