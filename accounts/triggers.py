#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from django.contrib import auth

from registration import signals

def login_on_activation(sender, user, request, **kwargs):
    user.backend='django.contrib.auth.backends.ModelBackend'
    auth.login(request,user)
signals.user_activated.connect(login_on_activation)


def login_on_registration(sender, user, request, **kwargs):
    user.backend='django.contrib.auth.backends.ModelBackend'
    auth.login(request,user)
signals.user_registered.connect(login_on_registration)
