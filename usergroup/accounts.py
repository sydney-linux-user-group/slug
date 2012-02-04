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
PROVIDERS = {
    'Twitter': social_auth.backends.twitter.TwitterBackend,
    'Facebook': social_auth.backends.facebook.FacebookBackend,
    'Google' : social_auth.backends.google.GoogleBackend,
    'Yahoo': social_auth.backends.yahoo.YahooBackend,
    'LinkedIn': social_auth.backends.contrib.linkedin.LinkedinBackend,
    'FourSquare': social_auth.backends.contrib.foursquare.FoursquareBackend,
    'GitHub': social_auth.backends.contrib.github.GithubBackend,
}

# List of providers to show in the openid section
OPENID_PROVIDERS = {
    'wordpress': '',
    'myspace': 'Username',
    'aol': 'Username',
}


def login(request):
    """Displays login mechanism"""
    providers = PROVIDERS
    openid_providers = OPENID_PROVIDERS

    if request.user.is_authenticated():
        return HttpResponseRedirect('profile')
    else:
	return render_to_response('accounts/login.html', locals(), RequestContext(request))


@login_required
def profile(request):
    """Login complete view, displays user data"""
    last_login = request.session.get('social_auth_last_login_backend')
    return render_to_response('accounts/profile.html', locals(), RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('accounts/error.html', locals(), RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')
