# -*- coding: utf-8 -*-
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
    nombre = models.CharField(max_lengthi = 50, null = False, blanck = False)
    fecha = models.IntegerField(null = False, blanck = False)
    formula = models.CharField(max_length = 1, choices=FORMULA_CHOICES, null = False, blanck = False)
    elecciones = models.CharField(max_length = 1, choices=ELECCIONES_CHOICES, null = False, blanck = False)

    def __unicode__(self):
        return self.nombre


class Sitio(TransModel):
    nombre = models.CharField(max_length = 200, null = False, blanck = False)
    num_a_elegir = models.IntegerField(null = False, blanck = False)
    tipo = models.IntegerField(null = False, blanck = False)
    votos_contabilizados = models.IntegerField(null = False, blanck = False)
    votos_abstenciones = models.IntegerField(null = False, blanck = False)
    votos_nulos = models.IntegerField(null = False, blanck = False)
    votos_blancos = models.IntegerField(null = False, blanck = False)
    contenido_en = models.ForeignKey('self', null = True, blanck = False, related_name = 'sitios')

    def __unicode__(self):
        return self.nombre


class Partido(TransModel):
    sistema = models.ForeignKey(Sistema, null = False, blanck = False, related_name = 'partidos')
    sitio = models.ForeignKey(Sitio, null = False, blanck = False, related_name = 'partidos')
    id_partido = models.IntegerField(null = False, blanck = False)
    nombre = models.CharField(max_length = 200, null = False, blanck = False)
    electos = models.IntegerField(null = False, blanck = False)
    votos_numero = models.IntegerField(null = False, blanck = False)
    votos_porciento = models.DecimalField(max_digits = 5, decimal_places = 2, null = False, blanck = False)
    residuo = models.IntegerField(null = True, blanck = False)

    def __unicode__(self):
        return self.nombre

