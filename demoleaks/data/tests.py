"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

from django.test import TestCase
#from demoleaks.data.models import Place,Election,Result,Party,ResultParties
from demoleaks.data.models import Place,Result


class ModelTest(TestCase):
    fixtures = ['2011.json']

    def test_votes_city(self):
        """
        Tests if all cities has the correct sum of diferent kind of votes (to a party,blank,null)
        """
        cities = Place.objects.filter(level=3) # level=3 -> provinces
        for i in cities:
            results = Result.objects.filter(place=i)
            for j in results:
                self.assertEqual(j.votes_parties + j.blank_votes + j.null_votes, j.total_voters)
                self.assertEqual(j.votes_parties + j.blank_votes, j.valid_votes)