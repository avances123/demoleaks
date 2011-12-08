# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Django admin tools
    #url(r'^admin_tools/', include('admin_tools.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Electoral formulas urls
    (r'', include('electoral.urls')),
)

# Serve user static files with the runserver in development
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
        )

# Added transhette url
if 'transhette' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
            url(r'^trans/', include('transhette.urls')),
        )
