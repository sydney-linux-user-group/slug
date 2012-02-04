from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth import views

from accounts.views import *

urlpatterns = patterns(
    'accounts',

    url(r'login/*$', views.login,
	{'template_name': 'login.html',
         'extra_context': {
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
    url(r'/', include('social_auth.urls')),
)
