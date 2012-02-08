from django.conf.urls.defaults import patterns, url, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # admin pages
    (r'^admin/', include(admin.site.urls)),
    # auth specific urls
    (r'^accounts/', include('accounts.urls')),
    # Our actual app
    (r'^', include('usergroup.urls')),
)
