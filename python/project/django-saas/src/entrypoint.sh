#!/bin/bash

if [ "$DJANGO_DEBUG" = "True" ]; then
    echo "Running in DEBUG mode. Pulling static files and collecting static files."
    python manage.py pull_staticfiles
    python manage.py collectstatic --noinput
else
    echo "Running in production mode. Skipping static file pulls."
fi

python manage.py runserver 0.0.0.0:8000