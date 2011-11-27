from lxml import etree
from operator import itemgetter, attrgetter  # Para ordenar listas
import csv

class Partido:
	def __init__(self,nombre,electos,votos_numero,votos_porciento):
		self.nombre = nombre
		self.electos = int(electos)
		self.votos_numero = int(votos_numero)
		self.votos_porciento = votos_porciento
		self.residuo = None # Variable para algunas formulas electorales

	def muestraInfo(self):
		print "==========================================="
		print "Partido: " + self.nombre 
		print "Electos: " + str(self.electos)
		print "Num Votos: " + str(self.votos_numero) 
		print "% De votos: " + self.votos_porciento
		if self.residuo != None:
			print "Residuo Hare: " + str(self.residuo)
		print "==========================================="
		

class Sitio:
	
	
	# Devuelve una lista de objetos partido
	def parseaPartidos(self,tree):
		lista_partidos=[]
		partidos = tree.xpath('/escrutinio_sitio/resultados/partido')
		for partido in partidos:
			nombre = partido.xpath('nombre')[0].text
			electos = partido.xpath('electos')[0].text
			votos_numero = partido.xpath('votos_numero')[0].text
			votos_porciento = partido.xpath('votos_porciento')[0].text
			p = Partido(nombre,electos,votos_numero,votos_porciento)
			lista_partidos.append(p)
		return lista_partidos
		

	def __init__(self, tree):
		# Numero de escanios a elegir
		self.num_a_elegir = int(tree.xpath('/escrutinio_sitio/num_a_elegir')[0].text)
		# Nombre de la circunscripcion
		self.nombre_sitio = tree.xpath('/escrutinio_sitio/nombre_sitio')[0].text
		
		# Primero parseamos la info de los votos del sitio
		self.contabilizados = int(tree.xpath('/escrutinio_sitio/votos/contabilizados/cantidad')[0].text)
		self.abstenciones = int(tree.xpath('/escrutinio_sitio/votos/abstenciones/cantidad')[0].text)
		self.nulos = int(tree.xpath('/escrutinio_sitio/votos/nulos/cantidad')[0].text)
		self.blancos = int(tree.xpath('/escrutinio_sitio/votos/blancos/cantidad')[0].text)
		self.total_votos = self.contabilizados + self.abstenciones + self.nulos + self.blancos
		# Despues parseamos la info por partidos
		self.lista_partidos = self.parseaPartidos(tree)
	


	


class Experimento:

	def __init__(self, sitio, nombre,fecha,formula,elecciones):
		self.sitio = sitio
		self.nombre = nombre
		self.fecha = fecha
		self.formula = formula
		self.elecciones = elecciones
		
	# De momento no implemento porque es como estan los datos originales
	def aplicaLeyDhont(self):
		pass

	def aplicaCocienteHare(self):
		#http://es.wikipedia.org/wiki/Cociente_Hare
		m = self.sitio.contabilizados
		n = self.sitio.num_a_elegir
		q = m / n
		electos_asignados = 0
		for partido in self.sitio.lista_partidos:
			partido.electos = partido.votos_numero / q
			partido.residuo = partido.votos_numero - q * partido.electos
			electos_asignados += partido.electos
		# Sea k el nmero de escaos que no son obtenidos por cociente:
		k = n - electos_asignados
		# Ordenamos de mayor a menor residuo y les sumamos un escano a los mejores de los k escanio
		partidos_ordenados = sorted(self.sitio.lista_partidos, key=attrgetter('residuo'), reverse=True)[0:k]
		print "Resumen Hare--------------"
		print "Escanios a repartir:" + str(self.sitio.num_a_elegir)
		print "Escanios fuera de cociente: " + str(k)
		for i in partidos_ordenados:
			i.electos += 1

	def muestraInfo(self):
		print "Nombre de la circunscripcion: " + self.sitio.nombre_sitio
		print "Total de escanios: " + str(self.sitio.num_a_elegir)
		print "Total de votos: " + str(self.sitio.total_votos)

		partidos_ordenados = sorted(self.sitio.lista_partidos, key=attrgetter('electos'), reverse=True)

		for i in self.sitio.lista_partidos:
			i.muestraInfo()

	
	def escribeCSV(self,path):
		# En este open hace falta un try catch
		writer = csv.writer(open(path, 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		partidos_ordenados = sorted(self.sitio.lista_partidos, key=attrgetter('votos_numero'), reverse=True)
		writer.writerow(['Partido','Diputados','Votos'])
		for i in partidos_ordenados:
			writer.writerow([i.nombre,i.electos,i.votos_numero])

	def escribeSQL(self,path):
		f = open(path, 'wb')
		f.write("INSERT INTO formulas_electorales_sistema (nombre, fecha, formula, elecciones) VALUES ('%s','%s','%s','%s');\n" % (self.nombre, self.fecha, self.formula, self.elecciones))
		f.close()	
	
	def insertaEnDB(self):
		from models import Sitio,Sistema,Partido
		conn = psycopg2.connect("dbname=django_sandbox user=fa")
		cur = conn.cursor()
		# Inserto datos del sistema
		cur.execute("INSERT INTO formulas_electorales_sistema (nombre, fecha, formula, elecciones) VALUES (%s, %s,%s, %s)",(self.nombre, self.fecha, self.formula, self.elecciones))
		conn.commit()





if __name__ == '__main__':

	#tree = etree.parse("http://rsl00.epimg.net/elecciones/2008/generales/congreso/index.xml2")
	tree = etree.parse("2011.xml")
	sitio = Sitio(tree)

	dhontExperimento = Experimento(sitio,'Generales 2011','2011-11-20','D','G')
	#dhontExperimento.aplicaCocienteHare()
	dhontExperimento.muestraInfo()
	dhontExperimento.escribeSQL('sql/2011.sql')
	#dhontExperimento.insertaEnDB()
	#dhontExperimento.escribeCSV('2008-dhont.csv')

#	sitio = Sitio(tree)
#	hareExperimento = Experimento(sitio,'Generales 2008 con coeficiente Hare')
#	hareExperimento.aplicaCocienteHare()
#	hareExperimento.muestraInfo()
#	hareExperimento.escribeCSV('2008-hare.csv')
#
#
