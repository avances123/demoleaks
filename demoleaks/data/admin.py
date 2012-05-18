from django.contrib.gis import admin
from models import Place,Party,Result,ResultParties

admin.site.register(Place, admin.OSMGeoAdmin)
admin.site.register(Party, admin.OSMGeoAdmin)
admin.site.register(Result, admin.OSMGeoAdmin)
admin.site.register(ResultParties, admin.OSMGeoAdmin)