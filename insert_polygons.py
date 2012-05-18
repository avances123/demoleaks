#!/usr/bin/python
#
# 
#

import psycopg2

level_table_map={
	1:'poligonos_ccaa',
	2:'poligonos_provincias',
	3:'poligonos_municipios',
	}

try:
#    conn = psycopg2.connect("dbname='demoleaks' user='fabio' host='localhost' password='dbpass'")
    conn1 = psycopg2.connect("dbname='demoleaks' user='fabio'")
    conn2 = psycopg2.connect("dbname='demoleaks' user='fabio'")
except:
    print "I am unable to connect to the database"

f = open('/tmp/places_not_imported.txt', 'w')
cur1 = conn1.cursor()
cur2 = conn2.cursor()
cur3 = conn1.cursor()

good = 0
bad = 0
x = 0
for level in xrange(1,4):
	print "level: %d, table: %s" % (level,level_table_map[level])
	cur1.execute("""SELECT name from data_place where level=%s order by name""",(level,))
	places = cur1.fetchall()
	total = len(places)
	for place in places:
		if level == 1:
			cur2.execute("""SELECT nombra,AsText(geom) from poligonos_ccaa where nombra = %s;""",(place[0],))
		elif level == 2:
			cur2.execute("""SELECT nombre,AsText(geom) from poligonos_provincias where nombre = %s;""",(place[0],))
		elif level == 3:
			cur2.execute("""SELECT municipio,AsText(geom) from poligonos_municipios where municipio = %s;""",(place[0],))
		res = cur2.fetchone()
		x = x + 1
		if res is None:
			bad = bad + 1
			f.write(place[0]+"\n")
			print "[%d/%d] BAD: %s" % (x,total,place[0])
		else:
			good = good + 1
			cur3.execute("""UPDATE data_place set polygon=GeomFromText(%s,4326) where name=%s;""",(res[1],res[0]))

conn1.commit()
cur1.close()
cur2.close()
cur3.close()

conn1.close()
conn2.close()


print "Malos: %d / %d" % (bad,total)
print "Buenos: %d / %d" % (good,total)
f.close()

