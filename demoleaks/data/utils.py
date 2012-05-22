# -*- coding: utf-8 -*-
from demoleaks.data.utils import *
import datetime,re,os,time,signal,sys
import urllib2,urllib,json


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



def mapping_checkpoint(mapfile,mapping_places):
    try:
        fp = open(mapfile, 'w+')
        json.dump(mapping_places, fp)
        fp.close()
        print "Checkpoint writed"
    except Exception as error:
        print error

def reconcile(name,level,mapping_places):
    try:
        return mapping_places[unicode(level)][name]
    except:
        pass
        
    data_request={'name':name.encode('utf-8'),'username':'avances123','lang':'es','type':'json','country':'ES','maxRows':1,'featureCode': "ADM%d" % level}
    print "http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request)
    geonames_response = urllib2.urlopen("http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request))
    geonames_object = json.load(geonames_response)
    time.sleep(2)
    try:
        geoname = geonames_object['geonames'][0]['toponymName']
        print "Added to mapping dict (ADM%d):  %s  ==>  %s" % (level,name,geoname)
        return geoname
    except:
        data_request['featureCode'] = 'A'
        geonames_response = urllib2.urlopen("http://api.geonames.org/searchJSON?" + urllib.urlencode(data_request))
        geonames_object = json.load(geonames_response)
        time.sleep(2)
        try:
            geoname = geonames_object['geonames'][0]['toponymName']
            print "Added to mapping dict (A):  %s  ==>  %s" % (name,geoname)
            return geoname
        except:
            print "GEONAMES ERROR: %s had no results" % name
            ferr = open('geonames_errors.csv','ab')
            ferr.write(name.encode('utf-8') + ',' + str(level) + '\n')
            ferr.close()
            return name  
