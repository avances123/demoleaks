from django.db import models

# Create your models here.

class Sistema(models.Model):
	nombre = models.CharField(max_length=200)
	#pub_date = models.DateTimeField('date published')


class Sitio(models.Model):
	sistema = models.ForeignKey(Sistema)
	nombre = models.CharField(max_length=200)
	votos = models.IntegerField()

class Partido(models.Model):
	sitio = models.ForeignKey(Sitio)
	nombre = models.CharField(max_length=200)

