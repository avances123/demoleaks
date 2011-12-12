# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from electoral.views.views import *

urlpatterns = patterns('electoral.views',
    # Home
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<sitio_id>\d+)/$', SitioView.as_view(), name='sitio'),
)
