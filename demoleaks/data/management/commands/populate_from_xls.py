# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from demoleaks.data.models import Place,Election,Result,Party,ResultParties
from openpyxl.reader.excel import load_workbook
import datetime,re,os,time,signal,sys
from optparse import make_option
import logging,urllib2,urllib,json


class Command(BaseCommand):
    args = u'filename'
    help = u'This command parses the xlsx files from Spanish Goverment, you can download them at http://bit.ly/IJol5A '
    digits = re.compile(r"^\d+")
    logging.basicConfig(level=logging.INFO)
    
    # Save dict if ctrl+c is pressed 
    def signal_handler(self,signal, frame): # El frame es necesario?
        print 'You pressed Ctrl+C, Saving mapping file...'
        write_cache(self.mapping_places) # Esto esta en demoleaks.data.utils
        sys.exit(0)

    def get_geoname(self,localname,level):
        signal.signal(signal.SIGINT, self.signal_handler) # A lo mejor esto solo hay que hacerlo una vez
        geoname = reconcile(localname,level,self.mapping_places) # O esta en el diccionario o lo pido a geonames
        time.sleep(2) 
        self.mapping_places[str(level)][localname] = geoname  # Meto clave valor en el dict
        return geoname            

    def get_type_of_election(self,filename):
        election_type = {
            '01': 'REFERENDUM',
            '02': 'NATIONAL', 
            '03': 'SENATE',
            '07': 'SUPRANATIONAL', 
            'number_to_find': 'REGIONAL'
        }
        return election_type[filename.split('_')[0]]

    def get_date_of_election(self,filename):
        year = int(filename[3:7])
        month = int(filename[7:9])
        return datetime.datetime(year=year,month=month,day=22) # TODO falta el dia

    # Used for reading a cell suposed to be an integer
    def read_int_cell(self,cell):
        if self.digits.match(str(cell.value)):                    
            return cell.value
        else:
            return 0 # Y si hay letras?

    # MAIN PROGRAM
    def handle(self, *args, **options):
        filename = args[0]
        type = self.get_type_of_election(os.path.basename(filename))
        date = self.get_date_of_election(os.path.basename(filename))
        
        logging.info("Loading: %s ...",filename)
        wb = load_workbook(filename)
        ws = wb.get_active_sheet()
        numrows = ws.get_highest_row() - 6 # por que un 6?
        rowcount = 0
        logging.info("%d Rows to be parsed",numrows)
        

        election = Election(date=date,type=type)
        election.name = ws.cell(coordinate='A3').value.strip()
        try:
            election = Election.objects.get(name__exact=election.name)
        except Election.DoesNotExist:
            election.save()



        
        spain = Place.objects.get(id=1)
        

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
        

        logging.info("Saving Data ...")
        # BUCLE general (para cada fila...)
        for row in ws.rows[6:]:
            rowcount = rowcount + 1
            logging.info("[%d/%d]",rowcount,numrows)

            # Municipio
            raw_cod = row[1].value.rstrip().zfill(2) + row[3].value.rstrip().zfill(3)
            mun = Place.objects.get(cod_ine__exact=raw_cod)
                

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
                print "\tSaved " + res.place.name + " num votes " + str(res.valid_votes)

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


                        

            





            
