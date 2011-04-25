
import config
config.setup()

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
        response = response
      else:
        guests.append(response)

  return response, guests


class ShowResponsePage(webapp.RequestHandler):
  def get(self, eventid):
    ####################################################
    event = models.Event.get_by_id(long(eventid))
    if not event:
      self.redirect('/')
    current_user = openid_users.get_current_user()
    if not current_user:
      self.redirect('/')
      return
    ####################################################

    response, guests = GetResponses(event, current_user)

    logging.warn("%s %s" % (response, guests))

    self.response.out.write(render(
        'templates/response-show.html', locals()))


class FriendsResponsePage(webapp.RequestHandler):
  def get(self, eventid):
    ####################################################
    event = models.Event.get_by_id(long(eventid))
    if not event:
      self.redirect('/')
    current_user = openid_users.get_current_user()
    if not current_user:
      self.redirect('/')
      return
    ####################################################

    response, guests = GetResponses(event, current_user)
    self.response.out.write(render(
        'templates/response-friends.html', locals()))


class UpdateResponsePage(webapp.RequestHandler):

  def post(self, eventid):
    ####################################################
    event = models.Event.get_by_id(long(eventid))
    if not event:
      self.redirect('/')
    current_user = openid_users.get_current_user()
    if not current_user:
      self.redirect('/')
      return
    ####################################################

    response, guests = GetResponses(event, current_user)
    if response is not None:
      response.delete()

    response = models.Response(event=event, guest=False)
    response.attending = self.request.get('attending').lower() != 'no'
    response.put()

    for guest in guests:
      guest.delete()

    guest_names = self.request.get_all('guest_name')
    logging.info('guest_names %s', guest_names)
    guest_emails = self.request.get_all('guest_email')
    logging.info('guest_emails %s', guest_emails)
    assert len(guest_names) == len(guest_emails)

    for name, email in zip(guest_names, guest_emails):
      name, email = name.strip(), email.strip()
      if not name or not email:
        continue

      response = models.Response(event=event, guest=True)
      response.attending = True
      response.guest_name = name
      response.guest_email = email
      response.put()

    self.redirect('/event/%s/response/show' % event.key().id())

  get = post
