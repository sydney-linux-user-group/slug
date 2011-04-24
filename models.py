
import config
config.setup()

from google.appengine.ext import db

# Some clever namespaces to make it easier to understand.
from google.appengine.ext import db as appengine
from aeoid import users as openid


class Event(db.Model):
  """A single combination game."""
  created_by = appengine.UserProperty(auto_current_user_add=True, required=True)
  created_on = db.DateTimeProperty(auto_now_add=True, required=True)

  name = db.StringProperty(required=True)
  text = db.StringProperty(multiline=True)

  start = db.DateTimeProperty(required=True)
  end = db.DateTimeProperty(required=True)


class Announcement(db.Model):
  created_by = openid.UserProperty(auto_current_user_add=True, required=True)
  created_on = db.DateTimeProperty(auto_now_add=True, required=True)

  name = db.StringProperty(required=True)
  text = db.StringProperty(multiline=True)

  valid_until = db.DateTimeProperty(required=True)

  # If a approver exists, then it is approved.
  approver = appengine.UserProperty()


class LightningTalk(db.Model):
  created_by = openid.UserProperty(auto_current_user_add=True, required=True)
  created_on = db.DateTimeProperty(auto_now_add=True, required=True)

  name = db.StringProperty(required=True)
  text = db.StringProperty(multiline=True)

  # If a approver exists, then it is approved.
  approver = appengine.UserProperty()

  given_at = db.Reference(Event)


class Response(db.Model):
  created_by = openid.UserProperty(auto_current_user_add=True, required=True)
  created_on = db.DateTimeProperty(auto_now_add=True, required=True)

  event = db.ReferenceProperty(Event)

  attending = db.BooleanProperty(required=True, default=True)

  # If this is a guest, then we store their details here, otherwise we just use
  # the creater's details.
  guest = db.BooleanProperty(required=True, default=False)
  guest_name = db.StringProperty()
  guest_email = db.EmailProperty()
