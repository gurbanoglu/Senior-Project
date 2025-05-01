from django.apps import AppConfig

# This file includes application configuration
# for the "users" app by configuring its
# attributes.


class UsersConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'users'

	# Create a method to import signals.
	def ready(self):
		import users.signals

# 5