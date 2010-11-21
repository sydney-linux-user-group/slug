
import config

import datetime
import logging

from google.appengine.ext import webapp
from google.appengine.api import users as appengine_users
from aeoid import users as openid_users

import models
from utils.render import render

def GetResponseFragment(current_user):
  query = models.Response.gql(
      "WHERE created_by = :user AND event = :event",
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
      if not response.guest:
        response = response.created_by
      else:
        guests.append(response)

  arguments = {
      'response': response,
      'guests': guests,
      }

  logging.warn(arguments)

  return render('templates/fragments/response.html', arguments)


class ShowResponsePage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'

    current_user = openid_users.get_current_user()
    if not current_user:
      self.response.out.write('<html><body>User not logged in.</body></html>')
      return

    self.response.out.write("""\
<html>
  <head>
    <title>Response</title>
    <link rel="StyleSheet" href="/css/base.css" type="text/css" media="screen">
  </head>
  <body>
%s
  </body>
</html>""" % GetResponseFragment(current_user))


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

    response = models.Response(
        event=event, guest=True, attending=True,
        guest_email = "james@polley.org",
        guest_name = "James Polley")
    response.put()
