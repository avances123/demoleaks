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
    print "CHOOSE A NAME TO REPLACE [%s] " % name
    geonames_response = urllib2.urlopen("http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request))
    geonames_object = json.load(geonames_response)
    for x in geonames_object['geonames']:
        print "[%s] (%s) [ %s ] " % (x['geonameId'],x['fcode'],x['name'])
    rawid = raw_input("Which geonames id do you prefer to reconcile?: ")
    print "http://api.geonames.org/get?geonameId=%s&lang=es&username=avances123" % rawid
    geonames_response = urllib2.urlopen("http://api.geonames.org/get?geonameId=%s&lang=es&username=avances123" % rawid)
    xmldoc = minidom.parse(geonames_response)
    element = xmldoc.getElementsByTagName('name')[0]
    print "Usando [%s] en lugar de [%s]" % (element.firstChild.nodeValue,name)
    return element.firstChild.nodeValue

    


def reconcile(name,level,mapping_places):
    try:
        return mapping_places[unicode(level)][name]
    except:
        pass
        
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
    time.sleep(2)
    try:
        geoname = geonames_object['geonames'][0]['name']
        print "Added to mapping dict (ADM%d):  %s  ==>  %s" % (level,name,geoname)
        return geoname
    except:
        return ask_user(name)

