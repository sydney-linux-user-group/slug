from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',

    (r'^accounts/create_user/$', 'accounts.views.create_new_user', {}),
    (r'^accounts/login/$', 'accounts.views.login', {}),
    (r'^accounts/logout/$', 'accounts.views.logout', {}),
)
