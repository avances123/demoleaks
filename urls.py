from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
		    url(r'^$', 'formulas_electorales.views.index'),
		    url(r'^sistema/(?P<sistema_id>\d+)/$', 'formulas_electorales.views.sistema'),
		    url(r'^sitio/(?P<sistema_id>\d+)/(?P<sitio_id>\d+)/$', 'formulas_electorales.views.sitio'),
		  )
