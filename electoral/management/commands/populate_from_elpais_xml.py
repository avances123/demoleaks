# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.management.base import BaseCommand, CommandError

from  countries.models import Country
from electoral.models.models import *

import urllib
from xml.etree.ElementTree import parse
import datetime
from decimal import *

COMUNIDADES = [
    (1, 'ES-AN'),
    (2, 'ES-AR'),
    (3, 'ES-AS'),
    (4, 'ES-IB'),
    (5, 'ES-CN'),
    (6, 'ES-CB'),
    (7, 'ES-CM'),
    (8, 'ES-CL'),
    (9, 'ES-CT'),
    (10, 'ES-EX'),
    (11, 'ES-GA'),
    (12, 'ES-MD'),
    (13, 'ES-NC'),
    (14, 'ES-PV'),
    (15, 'ES-MC'),
    (16, 'ES-RI'),
    (17, 'ES-VC'),
    (18, 'ES-CE'),
    (19, 'ES-ML'),
]

PROVINCIAS = [
    (1, 'ES-C'),
    (2, 'ES-VI'),
    (3, 'ES-AB'),
    (4, 'ES-AL'),
    (5, 'ES-A'),
    (6, 'ES-O'),
    (7, 'ES-AV'),
    (8, 'ES-BA'),
    (9, 'ES-PM'),
    (10, 'ES-B'),
    (11, 'ES-BU'),
    (12, 'ES-CC'),
    (13, 'ES-CA'),
    (14, 'ES-S'),
    (15, 'ES-CS'),
    (16, 'ES-CR'),
    (17, 'ES-CO'),
    (18, 'ES-CU'),
    (19, 'ES-GI'),
    (20, 'ES-GR'),
    (21, 'ES-GU'),
    (22, 'ES-SS'),
    (23, 'ES-H'),
    (24, 'ES-HU'),
    (25, 'ES-J'),
    (26, 'ES-LO'),
    (27, 'ES-GC'),
    (28, 'ES-LE'),
    (29, 'ES-L'),
    (30, 'ES-LU'),
    (31, 'ES-M'),
    (32, 'ES-MA'),
    (33, 'ES-MU'),
    (34, 'ES-NA'),
    (35, 'ES-OR'),
    (36, 'ES-P'),
    (37, 'ES-PO'),
    (38, 'ES-SA'),
    (39, 'ES-TF'),
    (40, 'ES-SG'),
    (41, 'ES-SE'),
    (42, 'ES-SO'),
    (43, 'ES-T'),
    (44, 'ES-TE'),
    (45, 'ES-TO'),
    (46, 'ES-V'),
    (47, 'ES-VA'),
    (48, 'ES-BI'),
    (49, 'ES-ZA'),
    (50, 'ES-Z'),
]

class Command(BaseCommand):
    args = u'<populate_from_elpais year ...>'
    help = u'Populate database from ElPais.com XML file'

    def handle(self, *args, **options):
        if Sistema.objects.all().count() == 0:
            sistema = Sistema('Sistema D\'Hont')
            sistema.save()
        else:
            sistema = Sistema.objects.get(id=1)

        for year in args:   
            
            # Comicio
            pais = Country.objects.get(pk='ES') 
            comicio = Comicio(nombre=u'Elecciones Generales', pais=pais, tipo='G')

            # Pais
            url = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/index.xml2" % (int(year))
            sitio_pais = self._get_Sitio(url, sistema, codigo_ISO_3166='ES_es', parent=None)
            comicio.sitio = sitio_pais

            self.stdout.write(u'! Created comicio:\t%s\n' % comicio)
            comicio.save()

            # Comunidades
            for com in COMUNIDADES:
                urlc = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/%02d/index.xml2" % (int(year), com[0])
                sitio_comunidad = self._get_Sitio(urlc, sistema, codigo_ISO_3166=com[1], parent=sitio_pais)

                # Provincias
                for prov in PROVINCIAS:
                    urlp = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/%02d/%02d.xml2" % (int(year), 
                                        com[0], prov[0])
                    try:
                        sitio_provincia = self._get_Sitio(urlp, sistema, codigo_ISO_3166=prov[1], parent=sitio_comunidad)

                        # Municipios
                        errors = 0
                        for mun in range(1,2001): # I suppouse that a province has almost 2000 villages
                            urlm = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/%02d/%02d/%02d.xml2" % (int(year),
                                            com[0], prov[0], mun)
                            try:
                                sitio_municipio = self._get_Sitio(urlm, sistema, codigo_ISO_3166="", parent=sitio_provincia)
                                errors = 0  # Set errors to default value
                            except ParseError:
                                #self.stderr.write(u'E Parsing:\t%s\n' % urlm)
                                errors += 1
                                if errors > 9: break # if I found more than 10 consecutive error 

                    except ParseError:
                        #self.stderr.write(u'E Parsing:\t%s\n' % urlp)
                        pass
            
                
    def _get_Sitio(self, url, sistema, codigo_ISO_3166='', parent=None):
        tree = parse(urllib.urlopen(url)).getroot()

        # Sitio: Spain
        nombre = tree.find('nombre_sitio').text
        try:                    
            num_a_elegir = int(tree.find('num_a_elegir').text)
        except AttributeError:  # Municipios
            num_a_elegir = 0
        tipo = tree.find('tipo_sitio').text
        votos_contabilizados = int(tree.find('votos/contabilizados/cantidad').text)
        votos_abstenciones = int(tree.find('votos/abstenciones/cantidad').text)
        votos_nulos = int(tree.find('votos/nulos/cantidad').text)
        votos_blancos = int(tree.find('votos/blancos/cantidad').text)
        
        sitio = Sitio(nombre=nombre, num_a_elegir=num_a_elegir, tipo=tipo, votos_contabilizados=votos_contabilizados, 
                    votos_abstenciones=votos_abstenciones, votos_nulos=votos_nulos ,votos_blancos=votos_blancos, 
                    codigo_ISO_3166=codigo_ISO_3166, parent=parent,sistema=sistema)        
        sitio.save()
        self.stdout.write('! Created sitio:\t%s -> %s\n' % ((parent if parent else ""), sitio))

        tree_partidos = tree.findall('resultados/partido')
        for tree_partido in tree_partidos:
            id_partido = tree_partido.find('id_partido').text
            nombre =  tree_partido.find('nombre').text
            try:
                electos = tree_partido.find('electos').text
            except AttributeError:  # Municipios
                electos = 0
            votos_numero = tree_partido.find('votos_numero').text
            votos_porciento = tree_partido.find('votos_porciento').text
            
            partido = Partido(id_partido=int(id_partido), nombre=nombre, electos=int(electos), votos_numero=int(votos_numero), 
                            votos_porciento=Decimal(votos_porciento), sitio=sitio, sistema=sistema)
            partido.save()
            self.stdout.write('! Created partido:\t%s -> %s\n' % ((sitio if sitio else ''), partido))

        return sitio
