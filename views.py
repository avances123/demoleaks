from django.http import HttpResponse
from formulas_electorales.models import Sitio,Sistema,Partido
from django.template import Context, loader
from django.shortcuts import render_to_response


def index(request):
    	lista_sistemas = Sistema.objects.all()
	c = Context({'lista_sistemas': lista_sistemas,})
	return render_to_response('index.html',c)


    

def detail(request, sistema_id):
	return HttpResponse("You're looking at poll %s." % sistema_id)

