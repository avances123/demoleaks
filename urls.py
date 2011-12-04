from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
		    url(r'^$', 'formulas_electorales.views.index'),
		    url(r'^(?P<comicio_id>\d+)/$', 'formulas_electorales.views.comicio'),
		    url(r'^(?P<comicio_id>\d+)/(?P<sitio_id>\d+)/$', 'formulas_electorales.views.sitio'),
		  )

urlpatterns += staticfiles_urlpatterns()

