from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
		    url(r'^elecciones/$', 'formulas_electorales.views.index'),
		    url(r'^elecciones/(?P<sistema_id>\d+)/$', 'formulas_electorales.views.detail'),
		  )
