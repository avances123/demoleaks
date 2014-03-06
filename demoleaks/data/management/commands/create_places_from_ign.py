#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from demoleaks.data.models import Place
import osgeo.ogr
import os


IGN_MAPPING_CCAA = {
	'01':'61',
	'02':'62',
	'03':'63',
	'04':'64',
	'05':'65',
	'06':'66',
	'07':'67',
	'08':'68',
	'09':'69',
	'10':'70',
	'11':'71',
	'12':'72',
	'13':'73',
	'14':'74',
	'15':'75',
	'16':'76',
	'17':'77',
	'18':'51_ccaa',
	'19':'52_ccaa',
}

IGN_MAPPING_PROVS= {
	'33': '63',
	'39': '66',
	'31': '74',
	'26': '76',
	'28': '72',
	'07': '64',
	'30': '73',
	'51': '51_ccaa',
	'52': '52_ccaa',
	'38': '65',
	'35': '65',
	'05': '67',
	'09': '67',
	'24': '67',
	'34': '67',
	'37': '67',
	'40': '67',
	'42': '67',
	'47': '67',
	'49': '67',
	'15': '71',
	'27': '71',
	'36': '71',
	'32': '71',
	'01': '75',
	'20': '75',
	'48': '75',
	'50': '62',
	'22': '62',
	'44': '62',
	'08': '69',
	'17': '69',
	'25': '69',
	'43': '69',
	'12': '77',
	'46': '77',
	'03': '77',
	'06': '70',
	'10': '70',
	'04': '61',
	'11': '61',
	'14': '61',
	'18': '61',
	'21': '61',
	'23': '61',
	'29': '61',
	'41': '61',
	'16': '68',
	'13': '68',
	'02': '68',
	'19': '68',
	'45': '68'

}


class Command(BaseCommand):


	def handle(self, *args, **options):
		path = args[0]
		
		with Place.tree_objects.delay_mptt_updates():
			root = Place(name='España',polygon=None,cod_ine=0,parent=None)
			root.save()
			

			filename = os.path.join(path,'poligonos_ccaa_etrs89/poligonos_ccaa_etrs89.shp')
			shapeData = osgeo.ogr.Open(filename)
			layer = shapeData.GetLayer()

			for x in xrange(layer.GetFeatureCount()):
				feature = layer.GetFeature(x)
				geom = osgeo.ogr.ForceToMultiPolygon(feature.geometry())
				print "Creando %s" % feature.GetFieldAsString('nombre')
				com = Place(
					name    = feature.GetFieldAsString('nombre'),
					cod_ine = IGN_MAPPING_CCAA[feature.GetFieldAsString('cod_ccaa')],
					polygon = geom.ExportToWkt(),
					parent  = root
				)
				com.save()

			filename = os.path.join(path,'poligonos_provincia_etrs89/poligonos_provincia_etrs89.shp')
			shapeData = osgeo.ogr.Open(filename)
			layer = shapeData.GetLayer()

			for x in xrange(layer.GetFeatureCount()):
				feature = layer.GetFeature(x)
				geom = osgeo.ogr.ForceToMultiPolygon(feature.geometry())
				print "Creando %s" % feature.GetFieldAsString('nombre')
				parent = Place.objects.get(cod_ine=IGN_MAPPING_PROVS[feature.GetFieldAsString('codine')])
				com = Place(
					name    = feature.GetFieldAsString('nombre'),
					cod_ine = feature.GetFieldAsString('codine'),
					polygon = geom.ExportToWkt(),
					parent  = parent
				)
				com.save()


			filename = os.path.join(path,'poligonos_municipio_etrs89/poligonos_municipio_etrs89.shp')
			shapeData = osgeo.ogr.Open(filename)
			layer = shapeData.GetLayer()

			for x in xrange(layer.GetFeatureCount()):
				feature = layer.GetFeature(x)
				geom = osgeo.ogr.ForceToMultiPolygon(feature.geometry())
				print "Creando %s" % feature.GetFieldAsString('nombre')
				id_provincia = "%02d" % int(feature.GetFieldAsString('provincia'))
				parent = Place.objects.get(cod_ine=id_provincia)
				com = Place(
					name    = feature.GetFieldAsString('nombre'),
					cod_ine = feature.GetFieldAsString('codigoine'),
					polygon = geom.ExportToWkt(),
					parent  = parent
				)
				com.save()

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





