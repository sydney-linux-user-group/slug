#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from accounts import forms as login_forms
from accounts.views import *

from registration import views as register_views
from registration import forms as register_forms


urlpatterns = patterns(
    'accounts',

    url(r'login/*$', auth_views.login,
	    {'template_name': 'login.html',
         'authentication_form': login_forms.AuthenticationWithInActiveForm,
         'extra_context': {
            'register_form': register_forms.RegistrationFormUniqueEmail(),
	        'providers': PROVIDERS,
    	    'openid_providers': OPENID_PROVIDERS,
            },
        }),

    url(r'profile/*$', profile, name='profile'),
    url(r'profile/association/*$', profile, name='profile_associate'),
    url(r'profile/disconnected/*$', profile, name='profile_disconnect'),
    url(r'profile/new/*$', profile, name='profile_new'),
    url(r'error/*$', error, name='error'),
    url(r'logout/*$', logout, name='logout'),

    # These two URLs override two urls override the includes
    url(r'^register/*$', register_views.register,
        {'form_class': register_forms.RegistrationFormUniqueEmail,
         'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_register'),
    url(r'^activate/complete/$', lambda r: redirect('profile')),

    url(r'', include('social_auth.urls')),
    url(r'', include('registration.backends.default.urls')),
)
