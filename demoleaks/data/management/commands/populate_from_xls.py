# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from demoleaks.data.models import Place,Election,Result,Party,ResultParties
from demoleaks.data.utils import *
from openpyxl.reader.excel import load_workbook
import datetime,re,os,time,signal,sys
from optparse import make_option
import logging,urllib2,urllib,json

# File to save random names agains geonames
MAPFILE='geonames_map.json'


class Command(BaseCommand):
    args = u'filename'
    help = u'This command parses the xlsx files from Spanish Goverment, you can download them at http://bit.ly/IJol5A '
    digits = re.compile(r"^\d+")
    logging.basicConfig(level=logging.INFO)
    mapping_places={'1': {},'2': {},'3': {}}
    
    # Save dict if i press ctrl+c
    def signal_handler(self,signal, frame):
        print 'You pressed Ctrl+C, Saving mapping file...'
        mapping_checkpoint(MAPFILE,self.mapping_places)
        sys.exit(0)

    def get_geoname(self,localname,level):
        signal.signal(signal.SIGINT, self.signal_handler)
        geoname = reconcile(localname,level,self.mapping_places)  
        self.mapping_places[str(level)][localname] = geoname
        return geoname            

    def get_type_of_election(self,filename):
        election_type = {
            '02': 'NATIONAL', 
            '07': 'SUPRANATIONAL', 
            'number_to_find': 'LOCAL',
            'number_to_find': 'REGIONAL'

        }
        return election_type[filename.split('_')[0]]

    def get_date_of_election(self,filename):
        year = int(filename[3:7])
        month = int(filename[8:9])
        return datetime.datetime(year=year,month=month,day=22)

    # Used for reading a cell suposed to be an integer
    def read_int_cell(self,cell):
        if self.digits.match(str(cell.value)):                    
            return cell.value
        else:
            return 0

    # MAIN PROGRAM
    def handle(self, *args, **options):
               
        try:
            if not os.path.exists(MAPFILE):
                self.fp = open(MAPFILE, 'w+')
            else:
                self.fp = open(MAPFILE, 'r+')
            self.mapping_places = json.load(self.fp)
        except Exception as error:
            # Extra data: line 1 column 114 - line 1 column 406 (char 114 - 406)
            print "JSON ERROR: %s" % error
            sys.exit(1)

        filename = args[0]
        type = self.get_type_of_election(os.path.basename(filename))
        date = self.get_date_of_election(os.path.basename(filename))
        election = Election(date=date,type=type)
        logging.info("Loading: %s ...",filename)
        wb = load_workbook(filename)
        ws = wb.get_active_sheet()
        numrows = ws.get_highest_row() - 6
        rowcount = 0
        logging.info("%d Rows to be parsed",numrows)
        election.name = ws.cell(coordinate='A3').value.strip()
        election.save()

  
        raw_name = u'España'
        spain = Place(name=raw_name)
        try:
            spain = Place.objects.get(name__exact=spain.name)
        except Place.DoesNotExist:
            spain.save()
        

        # PARTIES
        # Save the party names into a dict
        logging.info("Saving Parties ...")
        parties_list = []
        for col in ws.columns[13:]:
            if col[4].value is not None:            
                name = col[4].value.rstrip()
            if col[5].value is not None:
                acro = col[5].value.rstrip()
            else:
                continue
            if acro != '':
                par = Party(acronym=acro,name=name,country=spain)
                try:
                    par = Party.objects.get(acronym__exact=acro,country=spain)
                except Party.DoesNotExist:
                    par.save()
                    logging.info("NEW PARTY: %s",name)
                parties_list.append(par)
        

        logging.info("Saving Places ...")
        x = 0
        # BUCLE general (para cada fila...)
        for row in ws.rows[6:]:
            x = x + 1
            if (x % 25 == 0):
                self.mapping_checkpoint()
            rowcount = rowcount + 1
            logging.info("[%d/%d]",rowcount,numrows)

            # Comunidad
            raw_name = row[0].value.rstrip()
            com = Place(name=self.get_geoname(raw_name,1),parent=spain)
            try:
                com = Place.objects.get(name__exact=com.name,parent=spain)
            except Place.DoesNotExist:
                com.save()

            # Provincia
            raw_name = row[2].value.rstrip()
            pro = Place(name=self.get_geoname(raw_name,2),parent=com)         
            try:
                pro = Place.objects.get(name__exact=pro.name, parent=com)
            except Place.DoesNotExist:
                pro.save()
            


            # Municipio
            raw_name = row[4].value.rstrip()
            mun = Place(name=self.get_geoname(raw_name,3), parent=pro)
            try:
                mun = Place.objects.get(name__exact=mun.name,parent=pro)
            except Place.DoesNotExist:                    
                mun.save()
                

            population = self.read_int_cell(row[5])
            num_tables = self.read_int_cell(row[6])
            total_census = self.read_int_cell(row[7])
            total_voters = self.read_int_cell(row[8])
            valid_votes = self.read_int_cell(row[9])
            votes_parties = self.read_int_cell(row[10])
            blank_votes = self.read_int_cell(row[11])
            null_votes = self.read_int_cell(row[12])

            
            res = Result(place=mun,election=election,population=population,num_tables=num_tables,
                            total_census=total_census,total_voters=total_voters,
                            valid_votes=valid_votes,votes_parties=votes_parties,
                            blank_votes=blank_votes,null_votes=null_votes)
            try:
                res = Result.objects.get(place__exact=mun,election__exact=election)
            except Result.DoesNotExist:
                res.save()
                #print "\tSaved " + res.place.name + " num votes " + str(res.valid_votes)

            # Resultado de los partidos
            num_col = 13 # En esta columna empiezan los partidos, espero
            for party in parties_list:
                num_votes = self.read_int_cell(row[num_col])
                if num_votes > 0:                    
                    respar = ResultParties(num_votes=num_votes,result=res,party=party)
                    try:
                        respar = ResultParties.objects.get(result__exact=res,party__exact=party)
                    except ResultParties.DoesNotExist:
                        respar.save()
                num_col = num_col + 1

        json.dump(self.mapping_places, self.fp)
        self.fp.close()

                        

            





            
