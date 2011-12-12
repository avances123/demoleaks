# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from electoral.views.views import *

urlpatterns = patterns('electoral.views',
    # Home
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<comicio_id>\d+)/$', ComicioView.as_view(), name='comicio'),
    url(r'^(?P<comicio_id>\d+)/(?P<sitio_id>\d+)/$', SitioView.as_view(), name='sitio'),
    url(r'^(?P<comicio_id>\d+)/(?P<sitio_id>\d+)/(?P<partido_id>\d+)/$', PartidoView.as_view(), name='partido'),
)
