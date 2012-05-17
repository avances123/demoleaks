#!/usr/bin/python
#
# 
#

import psycopg2

try:
#    conn = psycopg2.connect("dbname='demoleaks' user='fabio' host='localhost' password='dbpass'")
    conn1 = psycopg2.connect("dbname='demoleaks' user='fabio'")
    conn2 = psycopg2.connect("dbname='municipios' user='fabio'")
except:
    print "I am unable to connect to the database"

f = open('osm-errors.txt', 'w')
cur1 = conn1.cursor()
cur2 = conn2.cursor()
cur3 = conn1.cursor()

good = 0
bad = 0
x = 0

cur1.execute("""SELECT name from data_place where level=3 order by name""")
muns1 = cur1.fetchall()
total = len(muns1)
for mun in muns1:
	cur2.execute("""SELECT municipio,AsText(geom) from municipios_municipio where municipio = %s;""",(mun[0],))
	res = cur2.fetchone()
	x = x + 1
	#print "%d/%d" % (x,total)
	if res is None:
		bad = bad + 1
		print mun[0]
		f.write(mun[0]+"\n")
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

