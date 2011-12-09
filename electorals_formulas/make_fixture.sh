#!/bin/bash

python manage.py dumpdata --indent=4 electoral > electoral/fixtures/fixture_electoral.json
