
import config

import datetime
import logging

from google.appengine.ext import webapp
from google.appengine.api import users as appengine_users
from aeoid import users as openid_users

import models


class ShowResponsePage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'

    current_user = openid_users.get_current_user()
    if not current_user:
      self.response.out.write('User not logged in.')
      return

    query = models.Response.gql(
        "WHERE creator = :user AND event = :event",
        user = current_user._user_info_key,
        event = models.Event.get_by_id(1),
        )

    responses = query.fetch(100)

    response = None
    guests = []
    if len(responses) == 1:
      response = responses[0]
    elif len(responses) > 1:
      for response in responses:
        if not guest:
          response = response.creator
        else:
          guests.append(response)

    if response is None:
      self.response.out.write(
          "%s (%s) has yet to respond." % (
              current_user.nickname(), current_user.email()))

    elif response.attending:
      self.response.out.write(
          "%s (%s) is coming." % (
              response.creator.nickname(), response.creator.email()))

      for guest in guests:
        self.response.out.write(
            "with %s (%s)" % (
                guest.guest_name, guest.guest_email))

    else:
      self.response.out.write(
          "%s (%s) is not coming!" % (
              response.creator.nickname(), response.creator.email()))

      if guests:
        self.response.out.write(
            " And is somehow bring guests!?")


class AddResponsePage(webapp.RequestHandler):
  def get(self):

    admin = appengine_users.get_current_user()
    if admin is None:
      self.redirect(appengine_users.create_login_url(self.request.uri))
      return

    logging.warn('Admin %s', admin)

    event = models.Event.get_by_id(1)
    if event is None:
      event = models.Event(
          name = 'temp',
          text = 'desc',
          start = datetime.datetime.fromtimestamp(0),
          end = datetime.datetime.fromtimestamp(0),
          )
      event.put()

    current_user = openid_users.get_current_user()
    if current_user is None:
      self.redirect(openid_users.create_login_url(self.request.uri))
      return

    response = models.Response(
        event=event, guest=False, attending=True)
    response.put()
