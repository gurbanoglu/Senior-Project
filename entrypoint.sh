#!/bin/sh
set -e

# Ensure staticfiles directory exists
mkdir -p /app/django_project/staticfiles

# Run migrations
python manage.py migrate

# Collect static files without input
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
EOF

# Start the Gunicorn server
exec gunicorn django_project.wsgi:application --bind 0.0.0.0:8000