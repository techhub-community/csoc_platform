#!/bin/sh

python manage.py migrate --noinput --settings=csoc_backend.settings.local
python manage.py runserver --settings=csoc_backend.settings.local
