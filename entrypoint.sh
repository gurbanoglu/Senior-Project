#!/bin/sh
set -e

# Ensure staticfiles directory exists
mkdir -p /app/django_project/staticfiles

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn django_project.wsgi:application --bind 0.0.0.0:8000