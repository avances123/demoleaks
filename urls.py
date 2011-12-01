from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
		    url(r'^$', 'formulas_electorales.views.index'),
		    url(r'^(?P<sistema_id>\d+)/$', 'formulas_electorales.views.detail'),
		  )
