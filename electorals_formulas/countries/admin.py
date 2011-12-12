#!/usr/bin/env python
# -*- coding: utf-8 -*-

from countries.models import Country, Province
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

class CountryAdmin(TranslationAdmin):
    pass

admin.site.register(Country, CountryAdmin)

