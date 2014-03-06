from rest_framework import serializers
from demoleaks.data.models import Election


class ElectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Election
        #fields = ('id', 'name', 'description', 'date', 'main_photo', 'small_photo','medium_photo')
        #paginate_by = 10


        
        