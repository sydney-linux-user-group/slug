# Based on example code from:
#   http://en.gravatar.com/site/implement/images/python/

import urllib, hashlib

def gravatar(email, size=40):
  default = "/images/silhouette.png"

  # construct the url
  gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
  gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
  return gravatar_url
