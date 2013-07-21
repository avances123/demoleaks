# -*- coding: utf-8 -*-
from demoleaks.data.utils import *
import datetime,re,os,time,signal,sys
import urllib2,urllib,json
from xml.dom import minidom


def read_cache(mapfile='geonames_map.json'):
    try:
        if not os.path.exists(mapfile):
            fp = open(mapfile, 'w+')
            mapping_places={'1': {},'2': {},'3': {}}
        else:   
            fp = open(mapfile, 'r+')
            mapping_places = json.load(fp)
    except Exception as error:
        # Extra data: line 1 column 114 - line 1 column 406 (char 114 - 406)
        print "JSON ERROR: %s" % error
        sys.exit(1)
    return mapping_places

def write_cache(mapping_places,mapfile='geonames_map.json'):
    try:
        fp = open(mapfile, 'w+')
        json.dump(mapping_places, fp)
        fp.close()
        print "Checkpoint writed"
    except Exception as error:
        # Extra data: line 1 column 114 - line 1 column 406 (char 114 - 406)
        print "JSON ERROR: %s" % error
        sys.exit(1)

def ask_user(name):
    data_request={
    'country':'ES',
    'name':name.encode('utf-8'),
    'username':'avances123',
    'lang':'es',
    'type':'json',
    'maxRows':10,
    'featureCode': "A",
    #'fuzzy':'0.9',
    }
    print
    print "CHOOSE A NAME TO REPLACE [ %s ] " % name
    moredigits = re.compile(r".*\d{5};.*")
    if moredigits.match(name):
        return "ERROR"
    geonames_response = urllib2.urlopen("http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request))
    geonames_object = json.load(geonames_response)
    if len(geonames_object['geonames']) > 0:
        for x in geonames_object['geonames']:
            print "[%s] (%s) [ %s ] " % (x['geonameId'],x['fcode'],x['name'])
        rawid = raw_input("Insert geonameId or your own name record: ")
        digits = re.compile(r"^\d+")
        if digits.match(rawid):
            print "http://api.geonames.org/get?geonameId=%s&lang=es&username=avances123" % rawid
            geonames_response = urllib2.urlopen("http://api.geonames.org/get?geonameId=%s&lang=es&username=avances123" % rawid)
            xmldoc = minidom.parse(geonames_response)
            element = xmldoc.getElementsByTagName('name')[0]
            print "Using [%s] instead of [%s]" % (element.firstChild.nodeValue,name)
            print
            return element.firstChild.nodeValue
        else:
            print "Using [%s] instead of [%s]" % (rawid.decode('utf-8'),name)
            print
            return rawid.decode('utf-8')
    else:
        rawinput = raw_input("Enter the name manually: ")
        # TODO check input
        print "Using [%s] instead of [%s]" % (rawinput.decode('utf-8'),name)
        print
        return rawinput.decode('utf-8')

    


def reconcile(name,level,mapping_places):
	"""
	Intenta dar un geoname para nuestro string,
	si tiene varias opciones le pregunta al usuario
	"""
    try:
        return mapping_places[unicode(level)][name]
    except:
		# Es un string nuevo que no tenemos en el diccionario
        pass
     
	# Formamos un request para pedirselo a geonames
    data_request={
    'name':name.encode('utf-8'),
    'username':'avances123',
    'lang':'es',
    'type':'json',
    'country':'ES',
    'maxRows':1,
    'featureCode': "ADM%d" % level
    }
    #print "http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request)
    geonames_response = urllib2.urlopen("http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request))
    geonames_object = json.load(geonames_response)
    
    try:
        geoname = geonames_object['geonames'][0]['name']
        print "Added to mapping dict (ADM%d):  %s  ==>  %s" % (level,name,geoname)
        return geoname
    except:
        return ask_user(name)

