#!/usr/bin/python
# -*- coding: utf-8 -*-
from demoleaks.data.utils import *
import json,sys
import psycopg2

try:
    conn2 = psycopg2.connect("dbname='demoleaks' user='fabio'")
    conn1 = psycopg2.connect("dbname='ign' user='fabio'")
except:
    print "I am unable to connect to the database"

cur1 = conn1.cursor()
cur2 = conn2.cursor()

mapping_places = read_cache()

mapp
sqls={
    1:"""SELECT nombra,AsText(the_geom) from ccaa""",
    2:"""SELECT nombre,AsText(the_geom) from provincias""",
    3:"""SELECT municipio,AsText(the_geom) from municipios""",
}


x = 0
for level in sqls.keys():
    cur1.execute(sqls[level])
    places = cur1.fetchall()
    total = len(places)
    for place in places:
        rawname = place[0].decode('utf-8')
        #rawname = place[0]
        geom = place[1]
        name = reconcile(rawname,level,mapping_places)
        mapping_places[str(level)][rawname] = name
        x = x + 1
        if (x % 25 == 0):
            write_cache(mapping_places)

        cur2.execute("""UPDATE data_place set polygon=GeomFromText(%s,4326) where name=%s and level=%s;""",(geom,name,level))
        if cur2.rowcount == 0:
            print "Place not found: %s skiping update" % name
            continue
        else:
            print "Place found: %s, updating polygon" % name
        conn2.commit()

write_cache(mapping_places)
cur1.close()
conn1.close()
cur2.close()
conn2.close()
