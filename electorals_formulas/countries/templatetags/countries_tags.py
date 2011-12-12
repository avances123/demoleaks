#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter
from countries.models import *

register = template.Library()

def iso_flag(iso, flag_path=u''):
    """
    Returns a full path to the ISO 3166-1 alpha-2 country code flag image.
    
    Example usage::
    	
    	{{ user_profile.country.iso|iso_flag }}
    	
    	{{ user_profile.country.iso|iso_flag:"appmedia/flags/%s.png" }}
    
    """
    from countries.utils.isoflag import iso_flag
    return iso_flag(iso, flag_path)
iso_flag = stringfilter(iso_flag)

def iso3_to_name(iso3):
    """
    Returns the full name of a country from the iso3 name
    
    Example usage::
    	
    	{{ user_profile.country.iso|iso3_to_name }}
    	
    """
    if iso3:
        country = Country.objects.get(iso3=iso3)
        return country.printable_name
    else:
        return ""

# Syntax: register.filter(name of filter, callback)
register.filter('iso_flag', iso_flag)
register.filter('iso3_to_name', iso3_to_name)
