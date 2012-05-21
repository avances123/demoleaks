#!/usr/bin/python
#
# 
#
from demoleaks.data.utils import *
import json
import psycopg2

try:
    conn1 = psycopg2.connect("dbname='demoleaks' user='fabio'")
except:
    print "I am unable to connect to the database"

cur1 = conn1.cursor()

try:
    MAPFILE = 'geonames_map.json'
    if not os.path.exists(MAPFILE):
        fp = open(MAPFILE, 'w+')
    else:
        fp = open(MAPFILE, 'r+')
    mapping_places = json.load(fp)
except Exception as error:
    pass


sqls={
1:"""SELECT nombra,AsText(geom) from poligonos_ccaa""",
2:"""SELECT nombre,AsText(geom) from poligonos_provincias""",
3:"""SELECT municipio,AsText(geom) from poligonos_municipios""",
}

for level in sqls.keys():
    cur1.execute(sqls[level])
    places = cur1.fetchall()
    total = len(places)
    for place in places:
        rawname = place[0].decode('utf-8')
        geom = place[1]
        name = reconcile(rawname,level,mapping_places)
        mapping_places[level][rawname] = name
        cur1.execute("""UPDATE data_place set polygon=GeomFromText(%s,4326) where name=%s and level=%d;""",(geom,name,level))
    conn1.commit()

cur1.close()
conn1.close()
json.dump(mapping_places, fp)
fp.close()