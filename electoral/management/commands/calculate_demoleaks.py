# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.management.base import BaseCommand, CommandError
from decimal import *

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

        for sitio in Sitio.objects.filter(sistema=sistema):
            demoleak_sitio = 0
            if sitio.num_a_elegir > 0:
                for partido in sitio.partidos.all():
                    porcentaje_electos = ( Decimal(partido.electos) / Decimal(sitio.num_a_elegir)) * 100
                    print "porcentaje_electos %s = %s %s / %s %s * 100" % (porcentaje_electos,partido.nombre,partido.electos,sitio.nombre,sitio.num_a_elegir) 
                    partido.demoleak =  porcentaje_electos - partido.votos_porciento
                    partido.save()
                    if partido.demoleak > 0:
                        demoleak_sitio = demoleak_sitio + partido.demoleak
                print "%s %s" % (sitio,sitio.demoleak)
            sitio.demoleak = demoleak_sitio
            sitio.save()
