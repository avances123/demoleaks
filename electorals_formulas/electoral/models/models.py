# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Sistema(models.Model):
    FORMULA_CHOICES = (
            ('D', _(u'D\'hont')),
            ('H', _(u'Hare')),
        )
    ELECCIONES_CHOICES = ( 
            ('G', _(u'Generales')),
            ('A', _(u'Autonomicas')),
        )
    nombre = models.CharField(max_length=200, null=False, blank=False,
                verbose_name=_(u'Nombre'))
    fecha = models.DateField(null=False, blank=False,
                verbose_name=_(u'Fecha'))
    formula = models.CharField(max_length=1, choices=FORMULA_CHOICES, null=False, blank=False,
                verbose_name=_(u'Fórmula'))
    elecciones = models.CharField(max_length=1, choices=ELECCIONES_CHOICES, null=False, blank=False,
                verbose_name=_(u'Elecciones'))

    def __unicode__(self):
        return u'%s (%s - %s)' % (self.nombre, self.elecciones, self.fecha)

    class Meta:
        app_label = 'electoral'
        ordering = ['nombre', 'fecha',]
        verbose_name = _(u'Sistema Electoral')


class Comicio(models.Model):
    TIPO_CHOICES = (
            ('G', _(u'Generales')),
            ('S', _(u'Senado')),
            ('A', _(u'Autonomicas')),
            ('M', _(u'Municipales')),
        )

    nombre = models.CharField(max_length=200, null=False, blank=False,
                verbose_name=_(u'Nombre'))
    fecha = models.DateField(null=False, blank=False,
                verbose_name=_(u'Fecha'))
    pais = models.CharField(max_length=200, null=False, blank=False,
                    verbose_name=_(u'País'))
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, null=False, blank=False,
                    verbose_name=_(u'Tipo')) 

    def __unicode__(self):
        return u'%s (%s)' % (self.nombre, self.fecha)

    class Meta:
        app_label = 'electoral'
        ordering = ['fecha', 'pais', 'nombre']
        verbose_name = _(u'Comicio')


class Sitio(models.Model):
    comicio = models.ForeignKey(Comicio, null = True, blank = False, related_name = 'sitios',
                verbose_name=_(u'Comicio'))
    codigo_ISO_3166 = models.CharField(max_length = 8, null=True, blank = False,
                verbose_name=_(u'Código ISO 3166'))
    nombre = models.CharField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Nombre'))
    num_a_elegir = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Número a elegir'))
    tipo = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Tipo'))
    votos_contabilizados = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Votos Contabilizados'))
    votos_abstenciones = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Abstenciones'))
    votos_nulos = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Votos Nulos'))
    votos_blancos = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Votos Blancos'))
    contenido_en = models.ForeignKey('self', null = True, blank = False, related_name = 'sitios',
                verbose_name=_(u'Contenido en'))

    def __unicode__(self):
        return "%s (%s)" % (self.nombre, self.comicio)

    class Meta:
        app_label = 'electoral'
        ordering = ['comicio','nombre',]
        verbose_name = _(u'Sitio')


class Partido(models.Model):
    sitio = models.ForeignKey(Sitio, null = False, blank = False, related_name = 'partidos',
                verbose_name=_(u'Sitio'))
    id_partido = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'ID Partido'))
    nombre = models.CharField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Nombre'))
    electos = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Electos'))
    votos_numero = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Número de votos'))
    votos_porciento = models.DecimalField(max_digits = 5, decimal_places = 2, null = False, blank = False,
                verbose_name=_(u'Porcentaje de votos'))
    residuo = models.IntegerField(null = True, blank = False,
                verbose_name=_(u'Residuo'))

    def __unicode__(self):
        return self.nombre

    class Meta:
        app_label = 'electoral'
        ordering = ['nombre','sitio']
        verbose_name = _(u'Partido')


