from django.apps import AppConfig

# This file includes application configuration for
# the "base" app by configuring its attributes.

# The name of the app that can be added to the
# "INSTALLED_APPS" dictionary inside:
# django_project/django_project/settings.py.


class BaseConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'base'

# 6