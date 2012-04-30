#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2

try:
#    conn = psycopg2.connect("dbname='demoleaks' user='fabio' host='localhost' password='dbpass'")
    conn1 = psycopg2.connect("dbname='demoleaks' user='fabio'")
    conn2 = psycopg2.connect("dbname='osm' user='fabio'")
except:
    print "I am unable to connect to the database"


cur1 = conn1.cursor()
cur2 = conn2.cursor()

cur1.execute("""SELECT name from data_place where level=3 order by name""")
muns1 = cur1.fetchall()
for mun in muns1:
	print "Municipio: " + mun[0]
	cur2.execute("""SELECT distinct(name) from planet_osm_polygon where name = %s and admin_level = '8';""",(mun[0],))
	res = cur2.fetchall()
	print res

