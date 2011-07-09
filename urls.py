from django.conf.urls.defaults import patterns, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # auth specific urls
    (r'^', include('accounts.urls')),

    # Our actual app
    (r'^', include('usergroup.urls')),
)
