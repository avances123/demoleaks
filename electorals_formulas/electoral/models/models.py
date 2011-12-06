# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Sistema(TransModel):
    FORMULA_CHOICES = (
            ('D', 'Dhont'),
            ('H', 'Hare'),
        )
    ELECCIONES_CHOICES = (
            ('G', 'Generales'),
            ('A', 'Autonomicas'),
        }
    nombre = models.CharField(max_lengthi = 50, null = False, blanck = False,
                verbose_name=_(u'Nombre'))
    fecha = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Fecha'))
    formula = models.CharField(max_length = 1, choices=FORMULA_CHOICES, null = False, blanck = False,
                verbose_name=_(u'Fórmula'))
    elecciones = models.CharField(max_length = 1, choices=ELECCIONES_CHOICES, null = False, blanck = False,
                verbose_name=_(u'Elecciones'))

    def __unicode__(self):
        return "%s (%s - %s)" % (self.nombre, self.elecciones, self.fecha)

    class Meta:
        app_label = 'electorals'
        translate = ('nombre', 'formula', 'elecciones',)
        ordering = ['fecha', 'elecciones', 'nombre', 'formula',]        
        verbose_name = _(u'Sistema Electoral')
        verbose_name_plural = _(u'Sistemas Electorales')


class Comicio(TransModel):
    nombre = models.CharField(max_length = 50, null = False, blanck = False,
                verbose_name=_(u'Nombre'))
    fecha = models.DateField(null = False, blanck = False,
                verbose_name=_(u'Fecha'))

    def __unicode__(self):
        return '%s (%s)' % (self.nombre, self.fecha)

    class Meta:
        app_label = 'electorals'
        translate = ('nombre',)
        ordering = ['fecha', 'nombre',]        
        verbose_name = _(u'Comicio')
        verbose_name_plural = _(u'Comicios')


class Sitio(TransModel):
    comicio = models.ForeignKey(Comicio, null = True, blanck = False, related_name = 'sitios',
                verbose_name=_(u'Comicio'))
    codigo_ISO_3166 = models.CharField(max_length = 8, null=True, blank = False,
                verbose_name=_(u'Código ISO 3166'))
    nombre = models.CharField(max_length = 200, null = False, blanck = False,
                verbose_name=_(u'Nombre'))
    num_a_elegir = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Número a elegir'))
    tipo = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Tipo'))
    votos_contabilizados = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Votos Contabilizados'))
    votos_abstenciones = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Abstenciones'))
    votos_nulos = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Votos Nulos'))
    votos_blancos = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Votos Blancos'))
    contenido_en = models.ForeignKey('self', null = True, blanck = False, related_name = 'sitios',
                verbose_name=_(u'Contenido en'))

    def __unicode__(self):
        return "%s (%s)" % (self.nombre, self.comicio)

    class Meta:
        app_label = 'electorals'
        translate = ('nombre',)
        ordering = ['comicio', 'nombre',]         
        verbose_name = _(u'Sitio')
        verbose_name_plural = _(u'Sitios')


class Partido(TransModel):
    sitio = models.ForeignKey(Sitio, null = False, blanck = False, related_name = 'partidos',
                verbose_name=_(u'Sitio'))
    id_partido = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'ID Partido'))
    nombre = models.CharField(max_length = 200, null = False, blanck = False,
                verbose_name=_(u'Nombre'))
    electos = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Electos'))
    votos_numero = models.IntegerField(null = False, blanck = False,
                verbose_name=_(u'Número de votos'))
    votos_porciento = models.DecimalField(max_digits = 5, decimal_places = 2, null = False, blanck = False,
                verbose_name=_(u'Porcentaje de votos'))
    residuo = models.IntegerField(null = True, blanck = False,
                verbose_name=_(u'Residuo'))

    def __unicode__(self):
        return self.nombre

    class Meta:
        app_label = 'electorals'
        translate = ('nombre',)
        ordering = ['sitio', 'nombre',]         
        verbose_name = _(u'Partido')
        verbose_name_plural = _(u'Partidos')


