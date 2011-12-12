from django.db import models
from django import forms

# Create your models here.

class Sistema(models.Model):

	FORMULA_CHOICES = (
		         	('D', 'Dhont'),
			 	('H', 'Hare'),
			 )


	nombre = models.CharField(max_length=50)
	formula = models.CharField(max_length=1, choices=FORMULA_CHOICES)

        def __unicode__(self):
		return self.nombre

class Comicio(models.Model):
	nombre = models.CharField(max_length=50)
	fecha = models.DateField()
	pais = models.CharField(max_length=200)
	tipo = models.CharField(max_length=200)  # TODO poner choices



class Sitio(models.Model):

	comicio = models.ForeignKey(Comicio)
	contenido_en = models.ForeignKey('self',null=True)

	codigo_ISO_3166 = models.CharField(max_length=8,null=True)
	nombre_sitio = models.CharField(max_length=200)
	num_a_elegir = models.IntegerField()
	tipo_sitio = models.IntegerField()
	votos_contabilizados = models.IntegerField()
	votos_abstenciones = models.IntegerField()
	votos_nulos = models.IntegerField()
	votos_blancos = models.IntegerField()
	demoleak = models.DecimalField(max_digits=5,decimal_places=2,null=True)

	def __unicode__(self):
		        return self.nombre_sitio
	

class Partido(models.Model):
	sistema = models.ForeignKey(Sistema)
	sitio = models.ForeignKey(Sitio)
	comicio = models.ForeignKey(Comicio)

	demoleak = models.DecimalField(max_digits=5,decimal_places=2,null=True)
	id_partido = models.IntegerField()
	nombre = models.CharField(max_length=200)
	electos = models.IntegerField()
	votos_numero = models.IntegerField()
	votos_porciento = models.DecimalField(max_digits=5,decimal_places=2)
	residuo = models.IntegerField(null=True)
	def __unicode__(self):
		return self.nombre


