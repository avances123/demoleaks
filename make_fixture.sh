#!/bin/bash

if [ "$1" == "--load" ]; then
    python manage.py loaddata electoral/fixtures/fixture_electoral.json
else
    python manage.py dumpdata --format=xml --indent=4 countries > countries/fixtures/initial_data.json
    python manage.py dumpdata --format=xml --indent=4 auth sites > electoral/fixtures/initial_data.json
    python manage.py dumpdata --format=xml --indent=4 electoral > electoral/fixtures/fixture_electoral.json
fi
