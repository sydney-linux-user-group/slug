#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


## Registration
#
#  New Token? ---No--> Logged in
#     |
#    Yes
#     \/
#  IsTrusted? ---No--> Create Unverified User --> Logged In
#     |
#    Yes
#     \/
#  Create Verified User
#     |
#     \/
#  Merge Accounts with same Email -----> Logged In

## Association flow
#    Yes
#     \/
#  IsTrusted? ---No--> Create Unverified User --> Logged In
#     |
#    Yes
#     \/
#  Create Verified User
#     |
#     \/
#  Merge Accounts (NewUser/OldUser) -----> Logged In


## Verification Flow
#
#  Key Exists ----No---> Error
#     |
#    Yes
#     \/
#  Convert user to Verified
#     |
#     \/
#  Merge Accounts with same Email -----> Logged In






class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # Primary email used for communication with the user
    primary = models.ForeignKey('UserEmail')

    def get_emails(self):
        emails = UserEmail.filter(user=self.user)


class UserEmail(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    note = models.TextField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    VERIFIED_BY_CHOICES = (
        ('T', 'Trusted source'),
        ('E', 'Emailed activation'),
        ('A', 'Admin verified'),
    )

    verified_on = models.DateTimeField(null=True, blank=True)
    verified_by = models.CharField(max_length=1 choices=VERIFIED_BY_CHOICES)

    verification_key = models.CharField(max_length=40)


from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserEmail.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)


def mark_email_as_verified_on_activation(sender, user, request, **kwargs):
    pass
signals.user_activated.connect(verify_email_on_activation)

def merge_on_activation(sender, user, request, **kwargs):
    pass
signals.user_activated.connect(merge_on_activation)


def verify_user(backend, user, details, **kw):
    """If the user looked in via a trusted backend, we activate the user.
    """
    email = details.get('email')

    email = user.get_profile().email_details(email)
    if backend in settings.TRUSTED_AUTHENTICATION_BACKENDS:
        email.verify('T')
        email.save()

        user.is_active = True
        user.save()
    else:
        rego = registration.models.RegistrationManager.create_profile(user)
        rego.send_verify_email()


def merge_by_email(backend, details, *args, **kwargs):
    """We merge together any verified users with the same email address."""
    email = details.get('email')

    users = [ue.user for ue in UserEmail.filter(email__eq=email, verified_by__ne=None)]
    if len(users) > 2:
        merge.merge_model_objects(users[0], users[1:])


