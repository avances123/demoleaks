#from django.db import models
from django.contrib.gis.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Para municipios es admin_level = 8
class Place(MPTTModel):
    name = models.CharField(max_length=80, unique=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    polygon = models.MultiPolygonField(null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Election(models.Model):
	ELECTION_TYPES = (
        ('SUPRANATIONAL', 'More than one country election'),
		('NATIONAL', 'Whole country election'),
    	('REGIONAL', 'Regional election'),
    	('LOCAL', 'City level election'),
   	)
   	name = models.CharField(max_length=150)
	date = models.DateTimeField('Date of the election')
	type = models.CharField(max_length=20, choices=ELECTION_TYPES)
	places = models.ManyToManyField(Place, through='Result')



class Party(models.Model):
    name = models.CharField(max_length=80)
    acronym = models.CharField(max_length=20)
    country = models.ForeignKey(Place) # Comprobar que es de level = 0


# Many2Many intermediate classes
class Result(models.Model):
    population = models.IntegerField()
    num_tables = models.IntegerField()
    total_census = models.IntegerField()
    total_voters = models.IntegerField()
    valid_votes = models.IntegerField()
    votes_parties = models.IntegerField()
    blank_votes = models.IntegerField()
    null_votes = models.IntegerField()

    place = models.ForeignKey(Place)
    election = models.ForeignKey(Election)
    parties = models.ManyToManyField(Party, through='ResultParties')
	

class ResultParties(models.Model):
    num_votes = models.IntegerField()
    
    result = models.ForeignKey(Result)
    party = models.ForeignKey(Party)
    
