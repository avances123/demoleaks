#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from electoral.models import *


class ComicioAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Comicio, ComicioAdmin)


class SitioAdmin(MPTTModelAdmin):
    search_fields = ['nombre', 'codigo_ISO_3166', 'tipo', 'parent__nombre']
    list_filter = ['tipo', 'parent__nombre']
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Sitio, SitioAdmin)


class SistemaAdmin(admin.ModelAdmin):
    search_fields = ['nombre',]
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Sistema, SistemaAdmin)


class PartidoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'sitio__nombre']
    list_filter = ['sitio__nombre']
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Partido, PartidoAdmin)

