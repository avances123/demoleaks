from formulas_electorales.models import Sistema,Sitio,Partido,Comicio
import datetime,os
from lxml import etree
from operator import itemgetter, attrgetter  # Para ordenar listas
import urllib2
from decimal import *


def parseaPartidos(comicio,sistema,sitio,tree):
        lista_partidos=[]
        partidos = tree.xpath('/escrutinio_sitio/resultados/partido')
	getcontext().prec = 3
	democracia_sitio = Decimal(0)
	suma_democracia = Decimal(0)
	num_partidos_procesados = 0
        for partido in partidos:
		electos = 0
                nombre = partido.xpath('nombre')[0].text
		try:
                	electos = partido.xpath('electos')[0].text
		except IndexError:
			electos = 0
                id_partido = partido.xpath('id_partido')[0].text
                votos_numero = partido.xpath('votos_numero')[0].text
                votos_porciento = partido.xpath('votos_porciento')[0].text
		if sitio.num_a_elegir > 0:
			porcentaje_electos = ( Decimal(electos) / Decimal(sitio.num_a_elegir) ) * 100
			demoleak =  porcentaje_electos - Decimal(votos_porciento)
			if demoleak > 0:
				suma_democracia = demoleak + suma_democracia
			demoleak = str(demoleak)
		else:
			demoleak = None

                p = Partido(sistema=sistema,id_partido=id_partido,sitio=sitio,nombre=nombre,electos=electos,
				votos_numero=votos_numero,votos_porciento=votos_porciento,comicio=comicio,demoleak=demoleak)
                p.save()
		num_partidos_procesados += 1

	sitio.demoleak = suma_democracia
	sitio.save()

def parseaSitio(comicio, sistema, tree, contenedor, iso=None):
        # Numero de escanios a elegir
	num_a_elegir = 0
	try:
        	num_a_elegir = int(tree.xpath('/escrutinio_sitio/num_a_elegir')[0].text)
	except IndexError:
		pass
        # Nombre de la circunscripcion
        nombre_sitio = tree.xpath('/escrutinio_sitio/nombre_sitio')[0].text
        tipo_sitio = tree.xpath('/escrutinio_sitio/tipo_sitio')[0].text
        
        # Primero parseamos la info de los votos del sitio
        contabilizados = int(tree.xpath('/escrutinio_sitio/votos/contabilizados/cantidad')[0].text)
        abstenciones = int(tree.xpath('/escrutinio_sitio/votos/abstenciones/cantidad')[0].text)
        nulos = int(tree.xpath('/escrutinio_sitio/votos/nulos/cantidad')[0].text)
        blancos = int(tree.xpath('/escrutinio_sitio/votos/blancos/cantidad')[0].text)

	# Creamos el sitio
	s = Sitio(
			nombre_sitio=nombre_sitio,num_a_elegir=num_a_elegir,tipo_sitio=tipo_sitio,comicio=comicio,codigo_ISO_3166=iso,
			votos_contabilizados=contabilizados,votos_abstenciones=abstenciones,votos_nulos=nulos,votos_blancos=blancos,contenido_en=contenedor
		)
	s.save()
	print "Guardado el sitio %s" % nombre_sitio 
        # Despues parseamos la info por partidos
        parseaPartidos(comicio,sistema,s,tree)
	return s
	print "\n"



codigos_autonomias={
	'1' : 'ES-AN',
	'2' : 'ES-AR',
	'3' : 'ES-AS',
	'4' : 'ES-IB',
	'5' : 'ES-CN',
	'6' : 'ES-CB',
	'7' : 'ES-CM',
	'8' : 'ES-CL',
	'9' : 'ES-CT',
	'10' : 'ES-EX',
	'11' : 'ES-GA',
	'12' : 'ES-MD',
	'13' : 'ES-NC',
	'14' : 'ES-PV',
	'15' : 'ES-MC',
	'16' : 'ES-RI',
	'17' : 'ES-VC',
	#'18' : 'ES-CE',
	#'19' : 'ES-ML',
}


codigos_provincias={
'1':'ES-C',
'2':'ES-VI',
'3':'ES-AB',
'4':'ES-AL',
'5':'ES-A',
'6':'ES-O',
'7':'ES-AV',
'8':'ES-BA',
'9':'ES-PM',
'10':'ES-B',
'11':'ES-BU',
'12':'ES-CC',
'13':'ES-CA',
'14':'ES-S',
'15':'ES-CS',
'16':'ES-CR',
'17':'ES-CO',
'18':'ES-CU',
'19':'ES-GI',
'20':'ES-GR',
'21':'ES-GU',
'22':'ES-SS',
'23':'ES-H',
'24':'ES-HU',
'25':'ES-J',
'26':'ES-LO',
'27':'ES-GC',
'28':'ES-LE',
'29':'ES-L',
'30':'ES-LU',
'31':'ES-M',
'32':'ES-MA',
'33':'ES-MU',
'34':'ES-NA',
'35':'ES-OR',
'36':'ES-P',
'37':'ES-PO',
'38':'ES-SA',
'39':'ES-TF',
'40':'ES-SG',
'41':'ES-SE',
'42':'ES-SO',
'43':'ES-T',
'44':'ES-TE',
'45':'ES-TO',
'46':'ES-V',
'47':'ES-VA',
'48':'ES-BI',
'49':'ES-ZA',
'50':'ES-Z',
}

def llenaSitios(sistema,comicio):
	# fase nacional
	nacional = None
	url = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/index.xml2" % (comicio.fecha.year)
	try: 
		tree = etree.parse(url)
		print "Parseado %s" % url
		nacional = parseaSitio(comicio,sistema,tree,nacional,'ES')
		path = "ficheros/%d/" % (comicio.fecha.year)
		if not os.path.exists(path):
			os.makedirs(path)
	except IOError:
		pass


	#return None   # Solo para Espana
	# procesa una comunidad
	for comunidad in range(1,18):
		url = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/%02d/index.xml2" % (comicio.fecha.year,comunidad)
		comu_obj = None
		try:
			tree = etree.parse(url)
			print "Parseado %s" % url
			comu_obj = parseaSitio(comicio,sistema,tree,nacional,codigos_autonomias[str(comunidad)])
			path = "ficheros/%d/%02d/" % (comicio.fecha.year,comunidad)
			if not os.path.exists(path):
				os.makedirs(path)

		except IOError:
			pass
		# procesa una provincia
		for provincia in range(1,53):
				prov = None
				url = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/%02d/%02d.xml2" % (comicio.fecha.year,comunidad,provincia)
				try:
					tree = etree.parse(url)
					print "Parseado %s" % url
					prov = parseaSitio(comicio,sistema,tree,comu_obj,codigos_provincias[str(provincia)])
					path = "ficheros/%d/%02d/%02d" % (comicio.fecha.year,comunidad,provincia)
					if not os.path.exists(path):
						os.makedirs(path)
				
				except IOError:
					continue
					#print "Error http: %s" % url
				# procesa un municipio
				rotos = 0 # municipios rotos
				for municipio in range(1,1000):  # Esperamos que no haya mas de 1000 pueblos en una provincia
					if rotos > 10:  # Si no existen 10 xmls seguidos podemos decir que hemos llegado al ultimo pueblo
						break
					url = "http://rsl00.epimg.net/elecciones/%d/generales/congreso/%02d/%02d/%02d.xml2" % (comicio.fecha.year,comunidad,provincia,municipio)
					try:
						tree = None
						path = "ficheros/%d/%02d/%02d/%02d.xml" % (comicio.fecha.year,comunidad,provincia,municipio)
						if os.path.exists(path):
							tree = etree.parse(path)
							print "Parseado %s" % path
						else:
							tree = etree.parse(url)
							print "Parseado %s" % url
							u = urllib2.urlopen(url)
							localFile = open(path, 'w')
							localFile.write(u.read())
							localFile.close()	

						s = parseaSitio(comicio,sistema,tree,prov)
						rotos = 0
							
					except IOError:
						print "Error http: %s" % url
						rotos += 1
						continue



def aplicaCoefHare(orig,dest):
	for s in Sitio.objects.filter(tipo_sitio__lte = 4): # Para todos los sitios mayores o iguales que provincia
	#for s in Sitio.objects.filter(id = 1):  # Solo para el conjunto del estado
		m = s.votos_contabilizados
		n = s.num_a_elegir
		q = m / n
		electos_asignados = 0
		for p in Partido.objects.filter(sitio = s):
			electos = p.votos_numero / q
			residuo = p.votos_numero - q * electos
	                electos_asignados += electos
			partido_hare = Partido(
					sistema=dest,sitio=s,id_partido=p.id_partido,nombre=p.nombre,
					electos=electos,votos_numero=p.votos_numero,votos_porciento=p.votos_porciento,
					residuo=residuo
					)
			partido_hare.save()
		k = n - electos_asignados
		partidos_ordenados = sorted(Partido.objects.filter(sitio = s).filter(sistema=dest), key=attrgetter('residuo'), reverse=True)[0:k]
		for i in partidos_ordenados:
			i.electos += 1
			i.save()







def llenaSistemasBase():
	c = Comicio(id=1,nombre='Generales 2011',fecha=datetime.date(2011,11,20),pais='Spain',tipo='Generales')
	s = Sistema(id=1,nombre='ley D\'Hont',formula='D')
	s.save()
	c.save()
	llenaSitios(s,c)

	c = Comicio(id=2,nombre='Generales 2008',fecha=datetime.date(2008,11,20),pais='Spain',tipo='Generales')
	s = Sistema(id=1,nombre='ley D\'Hont',formula='D')
	s.save()
	c.save()
	llenaSitios(s,c)



	
if __name__ == '__main__':
	llenaSistemasBase()

