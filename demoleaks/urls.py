from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from data.models import Place,Election,Result,ResultParties
from django.views.generic import TemplateView


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

class PlaceViewSet(viewsets.ModelViewSet):
    model = Place

class ElectionViewSet(viewsets.ModelViewSet):
    model = Election

class ResultViewSet(viewsets.ModelViewSet):
    model = Result

class ResultPartiesViewSet(viewsets.ModelViewSet):
    model = ResultParties

# Routers provide an easy way of automatically determining the URL conf
#router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register(r'users'  , UserViewSet)
router.register(r'groups' , GroupViewSet)
router.register(r'places' , PlaceViewSet)
router.register(r'elections' , ElectionViewSet)
router.register(r'results' , ResultViewSet)
router.register(r'resultsparties' , ResultPartiesViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demoleaks.views.home', name='home'),
    # url(r'^demoleaks/', include('demoleaks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name="base.html"),name="home"),

    url(r'^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #url(r'^', include('data.urls')),

)
