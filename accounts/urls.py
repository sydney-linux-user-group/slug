#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth import views

from accounts.views import *

from registration import forms as register_forms
from accounts import forms as login_forms


urlpatterns = patterns(
    'accounts',

    url(r'login/*$', views.login,
	    {'template_name': 'login.html',
         'authentication_form': login_forms.AuthenticationWithInActiveForm,
         'extra_context': {
            'register_form': register_forms.RegistrationFormUniqueEmail(),
	        'providers': PROVIDERS,
    	    'openid_providers': OPENID_PROVIDERS,
            },
        }),

    url(r'profile/*$', profile, name='profile'),
    url(r'profile/association/*$', profile, name='profile'),
    url(r'profile/disconnected/*$', profile, name='profile'),
    url(r'profile/new/*$', profile, name='profile'),
    url(r'error/*$', error, name='error'),
    url(r'logout/*$', logout, name='logout'),
    url(r'', include('social_auth.urls')),
    url(r'', include('registration.backends.default.urls'),
        {'form_class': register_forms.RegistrationFormUniqueEmail}),
)
