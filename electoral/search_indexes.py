import datetime
from haystack.indexes import *
from haystack import site
from electoral.models import Sitio


class SitioIndex(SearchIndex):
        nombre = CharField(document=True, use_template=True)
        def index_queryset(self):
            return Sitio.objects.all()

site.register(Sitio, SitioIndex)
