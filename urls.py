from django.conf.urls.defaults import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # admin pages
    (r'^admin/', include(admin.site.urls)),
    # auth specific urls
    (r'^accounts/', include('social_auth.urls')),
    # Our actual app
    (r'^', include('usergroup.urls')),
)
