#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn csoc_backend.wsgi:application -w 2 -b unix:/app/gunicorn.sock
