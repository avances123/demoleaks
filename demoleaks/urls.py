from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from data.models import Place,Election,Result
from data.views import PlaceViewSet



# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'places' , PlaceViewSet)


# Admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demoleaks.views.home', name='home'),
    # url(r'^demoleaks/', include('demoleaks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #url(r'^', include('data.urls')),

)
