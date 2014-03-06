from models import  Election,Place,Result,ResultParties
from serializers import ElectionSerializer
from rest_framework import viewsets




class ElectionViewSet(viewsets.ReadOnlyModelViewSet):

    """
    Api REST de SwapSerializer
    """
    model = Election
    serializer_class = ElectionSerializer




class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Place

class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    model = Result

class ResultPartiesViewSet(viewsets.ReadOnlyModelViewSet):
    model = ResultParties