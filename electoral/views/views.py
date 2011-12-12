# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.messages import error, success
from django.shortcuts import render_to_response, get_object_or_404

from electoral.models import *

class ComicioView(TemplateView):
    template_name = 'electoral/comicio.html'

    def get(self, request, comicio_id, *args, **kwargs):
        context = self.get_context_data(comicio_id)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self,comicio_id, **kwargs):
        comicio = get_object_or_404(Comicio,id=comicio_id)
        context = super(ComicioView,self).get_context_data(**kwargs)
        context.update({'comicio':comicio})
        return context




class SitioView(TemplateView):
    template_name = 'electoral/sitio.html'

    def get(self, request, sitio_id, *args, **kwargs):
        context = self.get_context_data(sitio_id)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self,sitio_id, **kwargs):
        sitio = get_object_or_404(Sitio,id=sitio_id)
        context = super(SitioView,self).get_context_data(**kwargs)
        context.update({'sitio':sitio})
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
        context = super(IndexView, self).get_context_data(**kwargs)


