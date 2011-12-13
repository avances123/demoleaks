# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.management.base import BaseCommand, CommandError

from  countries.models import Country
from electoral.models.models import *


class Command(BaseCommand):
    args = u'<calculate_demoleaks.py system_id ...>'
    help = u'Calculate demoleak index for a system_id'

    def handle(self, *args, **options):
        # Cambiar eso para pillar el sistema de los args
        if Sistema.objects.all().count() == 0:
            sistema = Sistema('Sistema D\'Hont')
            sistema.save()
        else:
            sistema = Sistema.objects.get(id=1)

        for partido in Partido.objects.filter(sistema=sistema):
            sitio = partido.sitio
            if sitio.num_a_elegir > 0:
                #if partido.demoleak == None: partido.demoleak = 0
                porcentaje_electos = ( partido.electos / sitio.num_a_elegir ) * 100
                partido.demoleak =  porcentaje_electos - partido.votos_porciento
                if partido.demoleak > 0:
                    sitio.demoleak = sitio.demoleak + partido.demoleak
                sitio.save()
                #print "%s %s, tiene un demoleak de %s %s" % (sitio.nombre,partido, str(sitio.demoleak),str(partido.demoleak))
                print "%s %s %s %s" % (sitio.nombre,sitio.id,partido.nombre,partido.id)
                partido.save()

