from demoleaks.data.models import Place
from demoleaks.data.serializers import PlaceSerializer
from rest_framework import viewsets


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer






