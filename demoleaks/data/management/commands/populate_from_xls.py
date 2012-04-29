# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from demoleaks.data.models import Place,Election,Result,Party,ResultParties
from openpyxl.reader.excel import load_workbook

import datetime,re,os
from decimal import *
    


class Command(BaseCommand):
    args = u'<populate_from_elpais year ...>'
    help = u'Populate database from www.elpais.com XML file'
    digits = re.compile(r"^\d+")
    prefixre = re.compile(r"^(.+)\s+\((.+)\).*$")

    def get_type_of_election(self,filename):
        election_type = {
            '02': 'NATIONAL', 
            '07': 'SUPRANATIONAL', 
            'jack': 'LOCAL'
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
        filename = args[0]
        type = self.get_type_of_election(os.path.basename(filename))
        date = self.get_date_of_election(os.path.basename(filename))
        election = Election(date=date,type=type)
        print "Parsing " + filename
        wb = load_workbook(filename)
        ws = wb.get_active_sheet()
        numrows = ws.get_highest_row() - 6
        rowcount = 0
        election.name = ws.cell(coordinate='A3').value.strip()
        election.save()
        print "Populating data of " + election.name
        

        # Save the party names into a dict
        parties_list = []
        for col in ws.columns[13:]:
            acro = col[5].value
            name = col[4].value
            if acro != '':
                par = Party(acronym=acro,name=name)
                try:
                    par = Party.objects.get(acronym__exact=acro)
                except Party.DoesNotExist:
                    par.save()
                    print "Saved " + name
                parties_list.append(par)

        for row in ws.rows[6:]:
            rowcount = rowcount + 1
            # Comunidad
            com = Place(name=row[0].value.rstrip())
            try:
                com = Place.objects.get(name__exact=com.name)
            except Place.DoesNotExist:
                com.save()
                print "Saved " + com.name


            # Provincia
            pro = Place(name=row[2].value.rstrip(), parent=com)
            try:
                pro = Place.objects.get(name__exact=pro.name)
            except Place.DoesNotExist:
                pro.save()
                print "Saved " + pro.name + " in " + com.name


            # Municipio
            name = row[4].value.rstrip()
            m = self.prefixre.match(name)
            if m is not None:
                main_name = m.group(1)
                prefix = m.group(2)
                name = prefix + ' ' + main_name
            mun = Place(name=name, parent=pro)
            print "[%d/%d]" % (rowcount,numrows)
            try:
                mun = Place.objects.get(name__exact=mun.name)
            except Place.DoesNotExist:
                mun.save()
                print "[%d/%d] New saved place: %s >> %s >> %s" % (rowcount,numrows,com.name,pro.name,mun.name)

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




            
