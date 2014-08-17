# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.views import NewMessagesFeed
from users.views import CreateUser

admin.autodiscover()

# Include external apps views
urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)

urlpatterns = patterns('core.views',
    url(r'^feed/$', NewMessagesFeed(),),
)

# Rynda-related patterns
urlpatterns += patterns('',
    url(r'^$', 'message.views.list', name='main-index'),
    url(r'^api/', include('api.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^organization/', include('organizations.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^t/(?P<slug>[a-z_0-9-]+)$', 'message.views.list'),
    url(r'^t/(?P<slug>)message/', include('message.urls')),
)

# Project description patterns
urlpatterns += patterns(
    '',
    url(r'info/$', 'core.views.infopages', name="infopages"),
    url(r'info/(?P<url>.*)/$', 'django.contrib.flatpages.views.flatpage', ),
)

# Account-related patterns
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^register$', CreateUser.as_view(), name='user-creation'),
    url(r'^login$', 'login',
        {'template_name': 'login.html'}, name='user-login'),
    url(r'^logout$', 'logout', name='user-logout'),
    url(r'^password/reset$', 'password_reset', name='user-password-reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm', name='user-password-reset-confirm'),
    url(r'^password/reset/complete$',
        'password_reset_complete', name='password_reset_complete'),
    url(r'^password/reset/done', 'password_reset_done', name="password_reset_done"),
)
