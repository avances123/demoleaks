# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.messages import error, success
from django.shortcuts import render_to_response, get_object_or_404

from electoral.models import *

class ComicioView(TemplateView):
    template_name = 'electoral/sitio.html'

    def get(self, request, comicio_id, *args, **kwargs):
        context = self.get_context_data(comicio_id)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self,comicio_id, **kwargs):
        #comicio = Comicio.objects.get(id=comicio_id)
        sitio = Sitio.objects.get(tipo=1,tree_id=comicio_id)
        top_partidos = sitio.partidos.all()[:7]
        hijos = sitio.get_children()
        context = super(ComicioView,self).get_context_data(**kwargs)
        context.update({'sitio':sitio})
        context.update({'top_partidos':top_partidos})
        context.update({'hijos':hijos})
        return context




class SitioView(TemplateView):
    template_name = 'electoral/sitio.html'

    def get(self, request,comicio_id,sitio_id, *args, **kwargs):
        context = self.get_context_data(comicio_id,sitio_id)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self,comicio_id,sitio_id, **kwargs):
        # Creamos las estructuras que necesitamos
        comicio = Comicio.objects.get(id=comicio_id)
        sitio = get_object_or_404(Sitio,id=sitio_id)
        top_partidos = sitio.partidos.all()[:7]
        hijos = sitio.get_children()
        lista_anomalias = Partido.objects.filter(demoleak__isnull=False).order_by('-demoleak')[:9]
        # Creamos el contexto con estas estructuras para pintarlas
        context = super(SitioView,self).get_context_data(**kwargs)
        context.update({'sitio':sitio})
        context.update({'top_partidos':top_partidos})
        context.update({'hijos':hijos})
        context.update({'lista_anomalias':lista_anomalias})
        return context


class PartidoView(TemplateView):
    template_name = 'electoral/partido.html'

    def get(self, request, partido_id, *args, **kwargs):
        context = self.get_context_data(partido_id)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self,partido_id, **kwargs):
        partido = get_object_or_404(Partido,id=partido_id)
        context = super(PartidoView,self).get_context_data(**kwargs)
        context.update({'partido':partido})
        return context




class IndexView(TemplateView):
    template_name = 'electoral/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        lista_comicios = Comicio.objects.all()
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'lista_comicios':lista_comicios})
        return context


