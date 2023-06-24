#!/bin/sh

python manage.py migrate --noinput --settings=csoc_backend.settings.local
