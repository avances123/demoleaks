from django.db import models

# Create your models here.

class Sistema(models.Model):

	FORMULA_CHOICES = (
		         	('D', 'Dhont'),
			 	('H', 'Hare'),
			 )
	ELECCIONES_CHOICES = (
		         	('G', 'Generales'),
			 	('A', 'Autonomicas'),
			 )


	nombre = models.CharField(max_length=200)
	fecha = models.DateTimeField('Fecha elecciones')
	formula = models.CharField(max_length=1, choices=FORMULA_CHOICES)
	elecciones = models.CharField(max_length=1, choices=ELECCIONES_CHOICES)


class Sitio(models.Model):
	sistema = models.ForeignKey(Sistema)
	nombre_sitio = models.CharField(max_length=200)
	num_a_elegir = models.IntegerField()
	tipo_sitio = models.IntegerField()
	votos_contabilizados = models.IntegerField()
	votos_abstenciones = models.IntegerField()
	votos_nulos = models.IntegerField()
	votos_blancos = models.IntegerField()
	

class Partido(models.Model):
	id_partido = models.IntegerField()
	sitio = models.ForeignKey(Sitio)
	nombre = models.CharField(max_length=200)
	electos = models.IntegerField()
	votos_numero = models.IntegerField()
	votos_porciento = models.DecimalField(max_digits=5,decimal_places=2)
