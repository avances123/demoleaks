# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from electoral.models import *


class SistemaTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Sistema, SistemaTranslationOptions)


class ComicioTranslationOptions(TranslationOptions):
    fields = ('nombre', 'pais')

translator.register(Comicio, ComicioTranslationOptions)


class SitioTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Sitio, SitioTranslationOptions)


class PartidoTranslationOptions(TranslationOptions):
    fields = ('nombre',)

translator.register(Partido, PartidoTranslationOptions)

