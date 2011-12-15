#!/bin/bash

# DROP DATABASE
echo  "drop database electorals_formulas; create database electorals_formulas;" | psql -U postgres

# CREATE DATABASE
echo no | python manage.py syncdb --migrate
exit
# POPULATE DATABASE FROM ELPAIS XMLS
if [ "$1" == "--populate" ]; then
    python manage.py populate_from_elpais_xml 2008 2011
else
    python manage.py loaddata electoral/fixtures/fixture_electoral.json
fi

# REGENERATE ALL.POs
#django-admin.py makemessages -a
