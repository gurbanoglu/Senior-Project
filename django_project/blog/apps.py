from django.apps import AppConfig

# This file includes application configuration for
# the "blog" app by configuring its attributes.

# The "BlogConfig" class was added under
# "INSTALLED_APPS" in:
# django_project/django_project/settings.py.


class BlogConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'blog'

# 3