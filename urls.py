from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/usergroup/',}),
    (r'^usergroup/', include('usergroup.urls')),

    # auth specific urls
    (r'^accounts/create_user/$', 'usergroup.views.create_new_user'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'usergroup/login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/usergroup/',}),

    # Examples:
    # url(r'^$', 'slug.views.home', name='home'),
    # url(r'^slug/', include('slug.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
