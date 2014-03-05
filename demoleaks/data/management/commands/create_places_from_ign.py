#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from demoleaks.data.models import Place
import osgeo.ogr

SQL = {
	# This st_union takes more than 10 minutes
	#0:"""SELECT 'España','0',st_AsText(st_union(st_simplifyPreserveTopology(geom,0.01))) from poligonos_ccaa_etrs89""",
	0:"""SELECT 'España','0',NULL from poligonos_ccaa_etrs89""",
	1:"""SELECT nombra,cod_ccaa,st_AsText(geom) from poligonos_ccaa_etrs89 where cod_ccaa = '%s'""",
	2:"""SELECT nombre,cod_provin,st_AsText(geom) from poligonos_provincias_etrs89 where cod_provin = '%s'""",
	3:"""SELECT municipio,cod_ine,st_AsText(geom) from poligonos_municipios_etrs89  where cod_ine ~ '^%s'""",
}

IGN_MAPPING = {
	'63':['33'],
	'66':['39'],
	'74':['31'],
	'76':['26'],
	'72':['28'],
	'64':['07'],
	'73':['30'],
	'51':['51'],
	'52':['52'],
	'65':['38','35'],
	'67':['05','09','24','34','37','40','42','47','49'],
	'71':['15','27','36','32'],
	'75':['01','20','48'],
	'62':['50','22','44'],
	'69':['08','17','25','43'],
	'77':['12','46','03'],
	'70':['06','10'],
	'61':['04','11','14','18','21','23','29','41'],
	'68':['16','13','02','19','45'],
}


class Command(BaseCommand):


	def handle(self, *args, **options):
		filename = args[0]
		shapeData = osgeo.ogr.Open(filename)
		layer = shapeData.GetLayer()
		
		with Place.tree_objects.delay_mptt_updates():
			root = Place(name='España',polygon=None,cod_ine=0,parent=None)
			root.save()
			
			for x in xrange(layer.GetFeatureCount()):
				feature = layer.GetFeature(x)
				geom = osgeo.ogr.ForceToMultiPolygon(feature.geometry())
				print feature.geometry().GetGeometryType()
				com = Place(
					name    = feature.GetFieldAsString('nombre'),
					cod_ine = feature.GetFieldAsString('cod_ccaa'),
					polygon = geom.ExportToWkt(),
					parent  = root
				)
				com.save()

				# for y in IGN_MAPPING[x]:
				# 	cur.execute(SQL[2] % y)
				# 	row  = cur.fetchone()
				# 	prov = Place(name=row[0],polygon=row[2],cod_ine=row[1],parent=com)
				# 	prov.save()

				# 	cur.execute(SQL[3] % y)
				# 	rows = cur.fetchall()
				# 	print "Guardando municipios de %s" % row[0]
				# 	for row in rows:
				# 		if row[1] == '22028-22106':
				# 			anso = Place(name='Ansó',polygon=row[2],cod_ine='22028',parent=prov)
				# 			fago = Place(name='Fago',polygon=row[2],cod_ine='22106',parent=prov)
				# 			anso.save()
				# 			fago.save()
				# 			continue
				# 		muni = Place(name=row[0],polygon=row[2],cod_ine=row[1],parent=prov) 
				# 		muni.save()





