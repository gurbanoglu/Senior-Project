from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
	help = "Creates a superuser from environment variables if one doesn't exist"

	def handle(self, *args, **kwargs):
		User = get_user_model()

		username = os.getenv('DJANGO_SUPERUSER_USERNAME')
		email = os.getenv('DJANGO_SUPERUSER_EMAIL')

		# Ensure the password is set
		password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

		if not User.objects.filter(username=username).exists():
			# Creating superuser with email and password from environment variables
			User.objects.create_superuser(
				username=username, email=email, password=password
			)

			self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
		else:
			self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))