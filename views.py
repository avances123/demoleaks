from django.http import HttpResponse
from formulas_electorales.models import Sitio,Sistema,Partido
from django.template import Context, loader
from django.shortcuts import render_to_response


def index(request):
    	lista_sistemas = Sistema.objects.all()
	c = Context({'lista_sistemas': lista_sistemas,})
	return render_to_response('index.html',c)

def sistema(request, sistema_id):
	# TODO explicar el algoritmo
	# TODO poner Espana por defecto
	sistema = Sistema.objects.get(id = sistema_id)
	sitio = Sitio.objects.get(id = 1)  # Spain
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema).order_by('-votos_numero')
	return HttpResponse("You're looking at poll %s." % sistema_id)


def sitio(request, sitio_id, sistema_id):
	# TODO hay que pillar justo el sitio o 404
	sitio = Sitio.objects.get(id = sitio_id)
	sistema = Sistema.objects.get(id = sistema_id)
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema).order_by('-votos_numero')
	c = Context({'sitio': sitio,'lista_partidos':lista_partidos})
	return render_to_response('sitio.html',c)

def partido(request, partido_id):
	return HttpResponse("You're looking at poll %s." % partido_id)

