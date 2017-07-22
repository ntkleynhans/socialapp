# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

app_name = 'socialapp'

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^verify_credentials/$', views.verify_credentials, name='verify_credentials'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^wall/$', views.wall, name='wall'),
]

