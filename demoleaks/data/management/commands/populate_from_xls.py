# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from demoleaks.data.models import Place,Election,Result,Party,ResultParties
from openpyxl.reader.excel import load_workbook

import datetime,re
from decimal import *
import time

class Command(BaseCommand):
    args = u'<populate_from_elpais year ...>'
    help = u'Populate database from www.elpais.com XML file'

    
    def handle(self, *args, **options):
        filename = args[0];
        election = Election(name=filename,date=datetime.datetime(year=2011,month=11,day=22),type='NATIONAL')
        election.save()
        print "Parsing " + filename
        wb = load_workbook(filename)
        ws = wb.get_active_sheet()

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
        print parties_list


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
            res = Result(place=mun,election=election,population=row[5].value or 0,
                            num_tables=row[6].value or 0,total_census=row[7].value or 0,total_voters=row[8].value or 0,
                            valid_votes=row[9].value or 0,votes_parties=row[10].value or 0,blank_votes=row[11].value or 0,
                            null_votes=row[12].value or 0)
            try:
                res = Result.objects.get(place__exact=mun,election__exact=election)
            except Result.DoesNotExist:
                res.save()
                print "Saving " + res.place.name + " num votes " + str(res.valid_votes)

            # Resultado de los partidos
            num_col = 13 # En esta columna empiezan los partidos, espero
            for party in parties_list:
                num_votes = row[num_col].value
                if num_votes != '':
                    respar = ResultParties(num_votes=row[num_col].value,result=res,party=party)
                    try:
                        respar = ResultParties.objects.get(result__exact=res,party__exact=party)
                    except ResultParties.DoesNotExist:
                        respar.save()
                        print "\tSaving " + party.name + " votes:" + str(num_votes)
                num_col = num_col + 1




            
