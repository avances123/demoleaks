from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from rest_framework import  routers
from django.views.generic import TemplateView
from demoleaks.data.views import ElectionViewSet,ResultViewSet,PlaceViewSet,ResultPartiesViewSet


# Routers provide an easy way of automatically determining the URL conf
#router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register(r'places' , PlaceViewSet)
router.register(r'elections' , ElectionViewSet)
router.register(r'results' , ResultViewSet)
router.register(r'resultsparties' , ResultPartiesViewSet)

admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name="base.html"),name="home"),

    url(r'^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #url(r'^', include('data.urls')),

)
