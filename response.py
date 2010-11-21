
import config

import datetime
import logging

from google.appengine.ext import webapp
from google.appengine.api import users as appengine_users
from aeoid import users as openid_users

import models
from utils.render import render

def GetResponses(event, user):
  query = models.Response.gql(
      "WHERE created_by = :user AND event = :event",
      user = user._user_info_key,
      event = event,
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

  return response, guests


class ShowResponsePage(webapp.RequestHandler):
  def get(self):
    ####################################################
    event = models.Event.get_by_id(1)
    current_user = openid_users.get_current_user()
    if not current_user:
      self.redirect('/')
      return
    ####################################################

    response, guests = GetResponses(event, current_user)

    self.response.out.write("""\
<html>
  <head>
    <title>Response</title>
    <link rel="StyleSheet" href="/css/base.css" type="text/css" media="screen">
  </head>
  <body>
%s
  </body>
</html>""" % render('templates/fragments/response.html', locals()))


class FriendsResponsePage(webapp.RequestHandler):
  def get(self):
    ####################################################
    event = models.Event.get_by_id(1)
    current_user = openid_users.get_current_user()
    if not current_user:
      self.redirect('/')
      return
    ####################################################

    response, guests = GetResponses(event, current_user)
    self.response.out.write(render(
        'templates/response-friends.html', locals()))


class UpdateResponsePage(webapp.RequestHandler):

  def post(self):
    ####################################################
    event = models.Event.get_by_id(1)
    current_user = openid_users.get_current_user()
    if not current_user:
      self.redirect('/')
      return
    ####################################################

    response, guests = GetResponses(event, current_user)
    if not response:
      response = models.Response(event=event, guest=False, attending=True)

    response.attending=self.request.get('attending').lower() == 'no'
    response.put()

    for guest in guests:
      guest.delete()

    guest_names = self.request.get_all('guest_name')
    logging.info('guest_names %s', guest_names)
    guest_emails = self.request.get_all('guest_emails')
    logging.info('guest_emails %s', guest_emails)
    assert len(guest_names) == len(guest_emails)

    for guest_name, guest_email in zip(guest_names, guest_emails):
      guest_name, guest_email = guest_name.strip(), guest_email.strip()
      if not guest_name or not guest_email:
        continue

      response = models.Response(event=event, guest=True)
      response.attending = True
      response.guest_name = name
      response.guest_email = email
      response.put()

    self.redirect('/')

  get = post
