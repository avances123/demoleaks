from rest_framework import serializers
from demoleaks.data.models import Place


class PlaceSerializer(serializers.ModelSerializer):


    class Meta:
        model = Place
        fields = ('id','name','cod_ine','parent')
