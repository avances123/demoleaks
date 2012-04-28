# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from demoleaks.data.models import Place,Election,Result,Party,ResultParties
from openpyxl.reader.excel import load_workbook

import datetime,re,os
from decimal import *
import time

class Command(BaseCommand):
    args = u'<populate_from_elpais year ...>'
    help = u'Populate database from www.elpais.com XML file'

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

    def handle(self, *args, **options):
        filename = args[0]
        type = self.get_type_of_election(os.path.basename(filename))
        date = self.get_date_of_election(os.path.basename(filename))
        election = Election(date=date,type=type)
        print "Parsing " + filename
        wb = load_workbook(filename)
        ws = wb.get_active_sheet()
        election.name = ws.cell(coordinate='A3').value.strip()
        election.save()

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
                    print "Saving " + name
                    par.save()
                parties_list.append(par)

        for row in ws.rows[6:]:
            # Comunidad
            com = Place(name=row[0].value.rstrip())
            try:
                com = Place.objects.get(name__exact=com.name)
            except Place.DoesNotExist:
                print "Saving " + com.name
                com.save()

            # Provincia
            pro = Place(name=row[2].value.rstrip(), parent=com)
            try:
                pro = Place.objects.get(name__exact=pro.name)
            except Place.DoesNotExist:
                print "Saving " + pro.name + " in " + com.name
                pro.save()

            # Municipio
            mun = Place(name=row[4].value.rstrip(), parent=pro)
            try:
                mun = Place.objects.get(name__exact=mun.name)
            except Place.DoesNotExist:
                mun.save()
                print "Saving " + mun.name + " in " + pro.name 

            # Resultado
            # population=row[5].value
            # num_tables = row[6].value
            # total_census = row[7].value
            # total_voters = row[8].value
            # valid_votes = row[9].value
            # votes_parties = row[10].value
            # blank_votes = row[11].value
            # null_votes = row[12].value
            if isinstance( row[5].value, int ):
                population = row[5].value
            else:
                population = 0
            if isinstance( row[6].value, int ):
                num_tables = row[6].value
            else:
                num_tables = 0
            if isinstance( row[7].value, int ):
                total_census = row[7].value
            else:
                total_census = 0
            if isinstance( row[8].value, int ):
                total_voters = row[8].value
            else:
                total_voters = 0
            if isinstance( row[9].value, int ):
                valid_votes = row[9].value
            else:
                valid_votes = 0
            if isinstance( row[10].value, int ):
                votes_parties = row[10].value
            else:
                votes_parties = 0
            if isinstance( row[11].value, int ):
                blank_votes = row[11].value
            else:
                blank_votes = 0
            if isinstance( row[12].value, int ):
                null_votes = row[12].value
            else:
                null_votes = 0
            
            res = Result(place=mun,election=election,population=population,num_tables=num_tables,
                            total_census=total_census,total_voters=total_voters,
                            valid_votes=valid_votes,votes_parties=votes_parties,
                            blank_votes=blank_votes,null_votes=null_votes)
            try:
                res = Result.objects.get(place__exact=mun,election__exact=election)
            except Result.DoesNotExist:
                res.save()
                print "Saving " + res.place.name + " num votes " + str(res.valid_votes)

            # Resultado de los partidos
            num_col = 13 # En esta columna empiezan los partidos, espero
            for party in parties_list:
                try:
                    num_votes = row[num_col].value
                    respar = ResultParties(num_votes=row[num_col].value,result=res,party=party)
                    try:
                        respar = ResultParties.objects.get(result__exact=res,party__exact=party)
                    except ResultParties.DoesNotExist:
                        respar.save()
                        print "\tSaving " + party.name + " votes:" + str(num_votes)
                except:
                    pass
                num_col = num_col + 1




            
