# A "post_save" signal is to be executed
# when a new user is created.

# This signal will be executed after an
# object is saved.
from django.db.models.signals import post_save

# The "User" model will be sending the signal.
from django.contrib.auth.models import User

# A receiver is a function that receives
# a signal and performs a certain task.
from django.dispatch import receiver
from .models import Profile

'''
Each time a new user is created, a user
profile will be created for that new user.

receiver(signal, sender) When a user is
saved, "signal" will be received by "receiver".
"receiver" is the CreateProfile() function.'''
@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
	# If a user was created, then create a
	# Profile object with the user equal to
	# the instance of the user that was created.
	if created:
		'''
		The following line will automatically give
		each newly created user permission to access
		the administrator's page of the Django
		application.'''
		# instance.is_staff = True
		# instance.is_superuser = True

		Profile.objects.create(m_user=instance)

		instance.save()


@receiver(post_save, sender=User)
def SaveProfile(sender, instance, **kwargs):
	# "instance" is the user.
	instance.profile.save()

# 16