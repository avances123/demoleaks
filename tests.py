"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from formulas_electorales.models import Sitio,Sistema,Partido

class SitioTest(TestCase):
    def comprueba_votos_totales(self):
        """
        Prueba que la suma de validos, blancos y nulos salgan todos.
	"""
	for s in Sitio.objects.all():
		suma_votos = 0
		for p in Partido.objects.filter(sitio = s):
			suma_votos += p.votos_numero

        	self.assertEqual(suma_votos, s.votos_contabilizados)

    def comprueba_suma_electos(self):
        """
        Prueba que la suma de diputados de cada partido es la misma que 
	la disponible para la circunscripcion
	"""
	for s in Sitio.objects.filter(tipo_sitio__lte = 4):
		suma_electos = 0
		for p in Partido.objects.filter(sitio = s):
			suma_electos += p.electos

        	self.assertEqual(suma_electos, s.num_a_elegir)
