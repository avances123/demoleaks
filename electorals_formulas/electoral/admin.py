#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from electoral.models import *


class SistemaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sistema, SistemaAdmin)


class ComicioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comicio, ComicioAdmin)


class SitioAdmin(MPTTModelAdmin):
    pass 

admin.site.register(Sitio, SitioAdmin)


class PartidoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Partido, PartidoAdmin)

