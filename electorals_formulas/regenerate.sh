#!/bin/bash

# DROP DATABASE
echo  "drop database electorals_formulas; create database electorals_formulas;" | psql -U postgres

# CREATE DATABASE
echo no | python manage.py syncdb

# POPULATE DATABASE FROM ELPAIS XMLS
python manage.py populate_from_elpais_xml
