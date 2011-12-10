from django.http import HttpResponse
from formulas_electorales.models import Sitio,Sistema,Partido,Comicio
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.core.context_processors import csrf


	



def index(request):
    	lista_comicios = Comicio.objects.all()
	lista_anomalias = Partido.objects.filter(grado_democracia__isnull=False).order_by('-grado_democracia')[:5]
	print lista_anomalias
	print lista_comicios
	c = Context({'lista_comicios': lista_comicios,'lista_anomalias':lista_anomalias})
	print c
	return render_to_response('index.html',c)


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
	if sitio.contenido_en == None:
		continente = sitio
	else:
		continente = Sitio.objects.get(id = sitio.contenido_en.id)
	comicio = Comicio.objects.get(id = comicio_id)
	lista_sistemas = Sistema.objects.all()
	if muestra_sistema_id:
		sistema = Sistema.objects.get(id = muestra_sistema_id)
		lista_provincias = None
	else:
		sistema = Sistema.objects.get(id = 1)
		lista_provincias = Sitio.objects.filter(tipo_sitio = 3)
	lista_sitios = Sitio.objects.filter(contenido_en = sitio).order_by('nombre_sitio')
	print lista_sitios
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema,comicio=comicio).order_by('-votos_numero')[:5]
	lista_anomalias = Partido.objects.filter(comicio = comicio).filter(grado_democracia__isnull=False).order_by('-grado_democracia')[:5]
	for i in lista_anomalias:
		print i.nombre
		print i.sitio
	c = Context({'sitio': sitio,'lista_sitios':lista_sitios,'lista_partidos':lista_partidos,'comicio':comicio,'sitios':lista_provincias,'lista_sistemas':lista_sistemas,'continente':continente,'lista_anomalias':lista_anomalias})
	return render_to_response('sitio.html',c)





def partido(request, partido_id):
	return HttpResponse("You're looking at poll %s." % partido_id)


def comicio(request, comicio_id):
	comicio = Comicio.objects.get(id = comicio_id)
	sitio = Sitio.objects.get(contenido_en = None,comicio = comicio)  # Mayor continente
	if sitio.contenido_en == None:
		continente = sitio
	else:
		continente = Sitio.objects.get(id = sitio.contenido_en.id)
	comicio = Comicio.objects.get(id = comicio_id)
	lista_sistemas = Sistema.objects.all()
	sistema = Sistema.objects.get(id = 1)
	lista_sitios = Sitio.objects.filter(contenido_en = sitio).order_by('nombre_sitio')
	lista_partidos = Partido.objects.filter(sitio = sitio,sistema = sistema,comicio=comicio).order_by('-votos_numero')[:5]
	c = Context({'sitio': sitio,'lista_sitios':lista_sitios,'lista_partidos':lista_partidos,'comicio':comicio,'lista_sistemas':lista_sistemas,'continente':continente})
	return render_to_response('comicio.html',c)





################ Busquedas  ######################


def split_query_into_keywords(query):
    """Split the query into keywords,
    where keywords are double quoted together,
    use as one keyword."""
    keywords = []
    # Deal with quoted keywords
    while '"' in query:
        first_quote = query.find('"')
        second_quote = query.find('"', first_quote + 1)
        quoted_keywords = query[first_quote:second_quote + 1]
        keywords.append(quoted_keywords.strip('"'))
        query = query.replace(quoted_keywords, ' ')
    # Split the rest by spaces
    keywords.extend(query.split())
    return keywords

def search_for_keywords(keywords):
    """Make a search that contains all of the keywords."""
    posts = Sitio.objects.all()
    for keyword in keywords:
        posts = posts.filter(nombre_sitio__icontains=keyword)
    return posts

 
def buscar(request):
	c = {}
	c.update(csrf(request))
	print "Es valido"        
	if request.method == 'POST':
		form = SearchForm(request.POST)
    	if form.is_valid():
        	keywords = form.cleaned_data['keywords']
        	keyword_list = split_query_into_keywords(keywords)
        	posts = search_for_keywords(keyword_list)
        	if posts:
        		results = Sitio.objects.filter(field_istartswith=form.busqueda)
            
	return render_to_response('search.html', c)

    
