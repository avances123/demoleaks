#!/bin/bash

python manage.py dumpdata --indent=4 countries > countries/fixtures/initial_data.json
python manage.py dumpdata --indent=4 auth sites > electoral/fixtures/initial_data.json
python manage.py dumpdata --indent=4 electoral > electoral/fixtures/fixture_electoral.json