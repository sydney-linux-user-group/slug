#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.messages.api import get_messages

import social_auth.backends

# Add in a URL which can be used to check it this person is logged into that service
social_auth.backends.twitter.TwitterBackend.loggedin_test = 'https://twitter.com/account/use_phx?setting=false&amp;format=text'
social_auth.backends.facebook.FacebookBackend.loggedin_test = 'https://www.facebook.com/imike3'

# List of providers to show in the top section
PROVIDERS = (
    ('Google' , social_auth.backends.google.GoogleBackend),
    ('Facebook', social_auth.backends.facebook.FacebookBackend),
    ('Twitter', social_auth.backends.twitter.TwitterBackend),
    ('LinkedIn', social_auth.backends.contrib.linkedin.LinkedinBackend),
    ('Yahoo', social_auth.backends.yahoo.YahooBackend),
# FIXME: We don't have icons for these...
#    ('FourSquare', social_auth.backends.contrib.foursquare.FoursquareBackend),
#    ('GitHub', social_auth.backends.contrib.github.GithubBackend),
)

# List of providers to show in the openid section
OPENID_PROVIDERS = (
#  ("AOL", "screen name",  "http://openid.aol.com/<strong>username</strong>"),
#  ("MyOpenID", "user name", "http://<strong>username</strong>.myopenid.com/"),
  ("Flickr", "user name", "http://flickr.com/<strong>username</strong>/"),
  ("Technorati", "user name", "http://technorati.com/people/technorati/<strong>username</strong>/"),
  ("Wordpress", "blog name", "http://<strong>username</strong>.wordpress.com"),
  ("Blogger", "blog name", "http://<strong>username</strong>.blogspot.com/"),
  ("LiveJournal", "blog name", "http://<strong>username</strong>.livejournal.com"),
#  ("ClaimID", "user name", "http://claimid.com/<strong>username</strong>"),
#  ("Vidoop", "user name", "http://<strong>username</strong>.myvidoop.com/"),
#  ("Verisign", "user name", "http://<strong>username</strong>.pip.verisignlabs.com/"),
)


@login_required
def profile(request):
    """Login complete view, displays user data"""
    providers = PROVIDERS
    openid_providers = OPENID_PROVIDERS

    last_login = request.session.get('social_auth_last_login_backend')
    return render_to_response('profile.html', locals(), RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', locals(), RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')
