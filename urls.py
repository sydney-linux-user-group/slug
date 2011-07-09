from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # auth specific urls
    (r'^accounts/create_user/$', 'usergroup.views.create_new_user'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'usergroup/login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/usergroup/',}),

    (r'^.*$', include('usergroup.urls')),
)
