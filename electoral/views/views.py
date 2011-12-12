# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.messages import error, success
from django.shortcuts import render_to_response, get_object_or_404

from electoral.models import *


class SitioView(TemplateView):
    template_name = 'electoral/sitio.html'

    def get(self, request, sitio_id, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        sitio = get_object_or_404(Sitio,id=sitio_id)
        context = super(SitioView,self).get_context_data(**kwargs)
        context.update({'sitio':sitio})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


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

    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

