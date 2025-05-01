from django.apps import AppConfig

# This file includes application
# configuration for the "weather"
# app by configuring its attributes.


class WeatherConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'weather'

# 5