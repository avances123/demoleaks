# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from countries.models import *
from electoral.models import *

class CountryTranslationOptions(TranslationOptions):
        fields = ('name', 'printable_name')

translator.register(Country, CountryTranslationOptions)


class ComicioTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Comicio, ComicioTranslationOptions)


class SitioTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Sitio, SitioTranslationOptions)


class SistemaTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Sistema, SistemaTranslationOptions)


class PartidoTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Partido, PartidoTranslationOptions)

