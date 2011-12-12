#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from django.db import models


class Country(models.Model):
    """
    International Organization for Standardization (ISO) 3166-1 Country list
    
     * ``iso`` = ISO 3166-1 alpha-2
     * ``name`` = Official country names used by the ISO 3166/MA in capital letters
     * ``printable_name`` = Printable country names for in-text use
     * ``iso3`` = ISO 3166-1 alpha-3
     * ``numcode`` = ISO 3166-1 numeric
    
    Note::
        This model is fixed to the database table 'country' to be more general.
        Change ``db_table`` if this cause conflicts with your database layout.
        Or comment out the line for default django behaviour.
    
    """
    iso = models.CharField(verbose_name='ISO alpha-2', max_length=2, primary_key=True)
    name = models.CharField(verbose_name='Official name (CAPS)', max_length=128)
    printable_name = models.CharField(verbose_name='Country name', max_length=128)
    iso3 = models.CharField(verbose_name='ISO alpha-3', max_length=3, null=True)
    numcode = models.PositiveSmallIntegerField(verbose_name='ISO numeric', null=True)
    
    class Meta:
        app_label = 'countries'
        verbose_name = _('Country')
        ordering = ('name',)
        
    class Admin:
        list_display = ('printable_name', 'iso',)
        
    def __unicode__(self):
        return self.printable_name


class UsState(models.Model):
    """
    United States Postal Service (USPS) State Abbreviations
    
    Note::
        This model is fixed to the database table 'usstate' to be more general.
        Change ``db_table`` if this cause conflicts with your database layout.
        Or comment out the line for default django behaviour.
    
    """
    name = models.CharField(verbose_name='State name', max_length=50, null=False)
    abbrev = models.CharField(verbose_name='Abbreviation', max_length=2, null=False)

    class Meta:
        app_label = 'countries'
        verbose_name = _('US State')
        ordering = ('name',)

    class Admin:
        list_display = ('name', 'abbrev',)

    def __unicode__(self):
        return self.name


class Province(models.Model):
    """
    Provinces for any country
    """
    country = models.ForeignKey('Country', null=False, related_name="provinces", verbose_name=_('Country'))
    name = models.CharField(verbose_name='Province name', max_length=50, null=False)
    code = models.CharField(verbose_name='Code', max_length=5, null=False)
    
    class Meta:
        app_label = 'countries'
        verbose_name = _(u'Province')
        ordering = ['country','name']
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        list_display = ('country', 'name', 'code',)

