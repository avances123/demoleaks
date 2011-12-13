"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from electoral.models import Sitio,Sistema,Partido,Comicio
import sys

class SitioTest(TestCase):
    def test_comprueba_votos_totales(self):
        lista = Sitio.objects.all()
        print >> sys.stderr, lista
        for s in Sitio.objects.all():
            print >> sys.stderr, "Haciendo el sitio"
            suma_votos = 0
            for p in Partido.objects.filter(sitio = s):
                suma_votos += p.votos_numero
                self.assertEqual(suma_votos, s.votos_contabilizados)

    def test_comprueba_suma_electos(self):
        for s in Sitio.objects.filter(tipo__lte = 4):
            suma_electos = 0
            for p in Partido.objects.filter(sitio = s):
                suma_electos += p.electos
                self.assertEqual(suma_electos, s.num_a_elegir)
