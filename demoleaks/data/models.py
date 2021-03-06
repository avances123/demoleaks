#from django.db import models
from django.contrib.gis.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from django.utils.encoding import force_unicode


# Para municipios es admin_level = 8
class Place(MPTTModel):
    name    = models.CharField(max_length=80, unique=False)
    cod_ine = models.CharField(max_length=15,unique=True)
    parent  = TreeForeignKey('self', null=True, blank=True, related_name='children')
    polygon = models.MultiPolygonField(srid=4326,null=True, blank=True)
    objects = models.GeoManager()
    tree_objects = TreeManager()


    def __unicode__(self):
        return force_unicode(self.name)

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

    def __unicode__(self):
        return force_unicode(self.name)



class Party(models.Model):
    name = models.CharField(max_length=180)
    acronym = models.CharField(max_length=50)
    country = models.ForeignKey(Place) # Comprobar que es de level = 0

    def __unicode__(self):
        return force_unicode(self.name)


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
    parties = models.ManyToManyField(Party, through='ResultParties',related_name='results')

    def __unicode__(self):
        return force_unicode("Resultado de %s en %s" % (self.place,self.election))
    

class ResultParties(models.Model):
    num_votes = models.IntegerField()
    
    result = models.ForeignKey(Result,related_name='resultsparties')
    party = models.ForeignKey(Party,related_name='resultparties')
    
    def __unicode__(self):
        return force_unicode("Resultado de %s en %s" % (self.party,self.result.place))
    

