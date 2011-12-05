from django.http import HttpResponse
from formulas_electorales.models import Sitio,Sistema,Partido,Comicio
from django.template import Context, loader
from django.shortcuts import render_to_response



def index(request):
    	lista_comicios = Comicio.objects.all()
	c = Context({'lista_comicios': lista_comicios,})
	return render_to_response('index.html',c)

def comicio(request, comicio_id):
	comicio = Comicio.objects.get(id = comicio_id)
	sitio = Sitio.objects.get(id = 1)  # Spain
	sistema = Sistema.objects.get(id = 1)  # Ley Dhont
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema).order_by('-votos_numero')
	lista_comunidades = Sitio.objects.filter(tipo_sitio=2)
	lista_sistemas = Sistema.objects.all()
	c = Context({'lista_sistemas':lista_sistemas,'comicio':comicio,'sitio': sitio,'lista_partidos':lista_partidos,'sitios':lista_comunidades})
	return render_to_response('comicio.html',c)


def sistema(request,comicio_id,sitio_id, sistema_id):
	# TODO explicar el algoritmo
	sistema = Sistema.objects.get(id = sistema_id)
	sitio = Sitio.objects.get(id = sitio_id)  
	comicio = Comicio.objects.get(id = comicio_id)  
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema,comicio=comicio).order_by('-votos_numero')
	lista_sistemas = Sistema.objects.all()
	c = Context({'sitio': sitio,'lista_partidos':lista_partidos,'comicio':comicio,'lista_sistemas':lista_sistemas,'sistema':sistema})
	return render_to_response('sistema.html',c)


def sitio(request, sitio_id, comicio_id,muestra_sistema_id=None):
	# TODO hay que pillar justo el sitio o 404
	sitio = Sitio.objects.get(id = sitio_id)
	comicio = Comicio.objects.get(id = comicio_id)
	lista_sistemas = Sistema.objects.all()
	if muestra_sistema_id:
		sistema = Sistema.objects.get(id = muestra_sistema_id)
		lista_provincias = None
	else:
		sistema = Sistema.objects.get(id = 1)
		lista_provincias = Sitio.objects.filter(tipo_sitio = 3)
	lista_sitios = Sitio.objects.filter(contenido_en = sitio).order_by('nombre_sitio')
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema,comicio=comicio).order_by('-votos_numero')
	c = Context({'sitio': sitio,'lista_sitios':lista_sitios,'lista_partidos':lista_partidos,'comicio':comicio,'sitios':lista_provincias,'lista_sistemas':lista_sistemas})
	return render_to_response('sitio.html',c)

def partido(request, partido_id):
	return HttpResponse("You're looking at poll %s." % partido_id)

