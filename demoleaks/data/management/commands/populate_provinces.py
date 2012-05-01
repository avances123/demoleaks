from django.core.management.base import BaseCommand, CommandError
from demoleaks.data.models import Place,Election,Result,Party,ResultParties

election = Election.objects.get(id=1)

class Command(BaseCommand):

    def sum_results(self,resultA,resultB):
        population = resultA.population + resultB.population
        num_tables = resultA.num_tables + resultB.num_tables
        total_census = resultA.total_census + resultB.total_census
        total_voters = resultA.total_voters + resultB.total_voters
        valid_votes = resultA.valid_votes + resultB.valid_votes
        votes_parties = resultA.votes_parties + resultB.votes_parties
        blank_votes = resultA.blank_votes + resultB.blank_votes
        null_votes = resultA.null_votes + resultB.null_votes
        return Result(place=resultB.place,election=election,population=population,num_tables=num_tables,
                                total_census=total_census,total_voters=total_voters,
                                valid_votes=valid_votes,votes_parties=votes_parties,
                                blank_votes=blank_votes,null_votes=null_votes)


    def handle(self, *args, **options):
        for pais in Place.objects.filter(level=0):
            res_pais = Result(place=pais,election=election,population=0,num_tables=0,
                                    total_census=0,total_voters=0,
                                    valid_votes=0,votes_parties=0,
                                    blank_votes=0,null_votes=0)
            for comu in Place.objects.filter(parent=pais):
                res_comu = Result(place=comu,election=election,population=0,num_tables=0,
                                    total_census=0,total_voters=0,
                                    valid_votes=0,votes_parties=0,
                                    blank_votes=0,null_votes=0)
                for prov in Place.objects.filter(parent=comu):
                    res_prov = Result(place=prov,election=election,population=0,num_tables=0,
                                    total_census=0,total_voters=0,
                                    valid_votes=0,votes_parties=0,
                                    blank_votes=0,null_votes=0)
                    for mun in Place.objects.filter(parent=prov):
                        res_mun = Result.objects.get(place=mun,election=election)
                        res_prov = self.sum_results(res_mun,res_prov)
                    print "Guardando %s population: %d" % (res_prov.place,res_prov.population)
                    res_prov.save()
                    res_comu = self.sum_results(res_prov,res_comu)
                print "Guardando %s population: %d" % (res_comu.place,res_comu.population)
                res_comu.save()
                res_pais = self.sum_results(res_comu,res_pais)
            print "Guardando %s population: %d" % (res_pais.place,res_pais.population)
            res_pais.save()
