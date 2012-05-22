# -*- coding: utf-8 -*-
from demoleaks.data.utils import *
import datetime,re,os,time,signal,sys
import urllib2,urllib,json



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
        return mapping_places[str(level)][name]
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
            ferr = open('geonames_errors.log','ab')
            ferr.write(name + '\n')
            ferr.close()
            return name  
