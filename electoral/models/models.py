# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.template.defaultfilters import slugify

from countries.models import Country

class Comicio(models.Model):
    TIPO_CHOICES = (
            ('G', _(u'Generales')),
            ('S', _(u'Senado')),
            ('A', _(u'Autonomicas')),
            ('M', _(u'Municipales')),
        )

    nombre = models.CharField(max_length=200, null=False, blank=False,
                    verbose_name=_(u'Nombre'))
    slug = models.SlugField(max_length=200, null=False, blank=False,
                    verbose_name=_(u'Slug'))
    pais = models.ForeignKey(Country, null=False, blank=False, related_name='comicios',
                    verbose_name=_(u'Pais'))
    fecha = models.DateField(null=True, blank=False,
                    verbose_name=_(u'Fecha'))
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, null=False, blank=False,
                    verbose_name=_(u'Tipo')) 
    sitio = models.ForeignKey('Sitio', null = True, blank = False, related_name = 'comicios',
                    verbose_name=_(u'Sitio'))

    def __unicode__(self):
        return u'%s (%s)' % (self.nombre, self.fecha)

    class Meta:
        app_label = 'electoral'
        ordering = ['pais', 'nombre']
        verbose_name = _(u'Comicio')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Register a new user
            self.slug = slugify(self.nombre)

        super(Comicio, self).save(*args, **kwargs)


class Sistema(models.Model):
    nombre = models.CharField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Nombre'))
    slug = models.SlugField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Slug'))

    def __unicode__(self):
        return u'%s' % (self.nombre)

    class Meta:
        app_label = 'electoral'
        ordering = ['nombre','slug']
        verbose_name = _(u'Sistema')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Register a new user
            self.slug = slugify(self.nombre)

        super(Sistema, self).save(*args, **kwargs)



class Sitio(MPTTModel):
    codigo_ISO_3166 = models.CharField(max_length = 8, null=True, blank = False,
                verbose_name=_(u'Código ISO 3166'))
    nombre = models.CharField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Nombre'))
    slug = models.SlugField(max_length=200, null=False, blank=False,
                    verbose_name=_(u'Slug'))
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
    demoleak = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True,
                verbose_name=_(u'Demoleak'))
    parent = TreeForeignKey('self', null = True, blank = True, related_name = 'sitios',
                verbose_name=_(u'Contenido en'))
    sistema = models.ForeignKey('Sistema', null = False, blank = False, related_name = 'sitios',
                            verbose_name=_(u'Sistema'))

    def __unicode__(self):
        return u'%s' % self.nombre

    class MPTTMeta:
        order_insertion_by = ['nombre']

    class Meta:
        app_label = 'electoral'
        ordering = ['nombre']
        verbose_name = _(u'Sitio')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Register a new user
            self.slug = slugify(self.nombre)

        super(Sitio, self).save(*args, **kwargs)

    def comicio(self):
        return self.get_root().comicios.all()[0]



class Partido(models.Model):
    # El sitio donde particia este partido
    sitio = models.ForeignKey('Sitio', null = False, blank = False, related_name = 'partidos',
                verbose_name=_(u'Sitio'))
    # El sistema utilizado para los datos de este partido
    sistema = models.ForeignKey('Sistema', null = False, blank = False, related_name = 'partidos',
                            verbose_name=_(u'Sistema'))
    # Id del partido segun elpais.com
    id_partido = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'ID Partido'))
    nombre = models.CharField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Nombre'))
    slug = models.SlugField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Slug'))
    electos = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Electos'))
    votos_numero = models.IntegerField(null = False, blank = False,
                verbose_name=_(u'Número de votos'))
    votos_porciento = models.DecimalField(max_digits = 5, decimal_places = 2, null = False, blank = False,
                verbose_name=_(u'Porcentaje de votos'))
    demoleak = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True,
                verbose_name=_(u'Demoleak'))


    def __unicode__(self):
        return u'%s (%s)' % (self.nombre, self.sitio)

    class Meta:
        app_label = 'electoral'
        ordering = ['-votos_numero','sitio']
        verbose_name = _(u'Partido')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Register a new user
            self.slug = slugify(self.nombre)

        super(Partido, self).save(*args, **kwargs)


class Sistema(models.Model):
    nombre = models.CharField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Nombre'))
    slug = models.SlugField(max_length = 200, null = False, blank = False,
                verbose_name=_(u'Slug'))

    def __unicode__(self):
        return u'%s' % (self.nombre)

    class Meta:
        app_label = 'electoral'
        ordering = ['nombre',]
        verbose_name = _(u'Sistema')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Register a new user
            self.slug = slugify(self.nombre)

        super(Sistema, self).save(*args, **kwargs)
