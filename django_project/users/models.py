from django.db import models
from django.contrib.auth.models import User

# Importing "Image" aides in resizing images.
from PIL import Image

# Creating a new model and inheriting
# from 'models.Model'.


class Profile(models.Model):
	'''
	I passed "User" as the argument below
  because there needs to be a one-to-one
  relationship with the User model.
	"CASCADE" indicates that if the user is
  deleted, then delete the profile, but if
  the profile is deleted, the user won't
  be deleted.'''

	m_user = models.OneToOneField(
		User, on_delete=models.CASCADE,
		verbose_name="User")

	# 'profile_pics' will be the directory
	# where images get saved when a profile
	# image is uploaded.
	m_Profile_Image = models.ImageField(
		default='DefaultProfileImage.jpg',
		upload_to='profile_pics',
		verbose_name="Profile Image")

	m_Facial_Image = models.ImageField(
		default='DefaultFacialImage.jpg',
		upload_to='facial_images',
		verbose_name="Facial Image")

	# Anytime a profile is displayed, show
	# the username followed by "Profile".
	def __str__(self):
		return f'{self.m_user.username} Profile'

	class Meta:
		verbose_name = "Profile"
		verbose_name_plural = "Profiles"

	'''
	Override the "save()" method, so that a
	functionality can be added. "save()" is
	the method which will be executed after
	the model is saved.

	The following section is commented out
	so that images will not be automatically
	resized.'''
	# def save(self, *args, **kwargs):
	#			'''
	#     This will execute the "save()" method of
	# 		the parent class. The save() method must
	# 		accept arguments that the parent class
	#     might be expecting. 'args' is for positional
	# 		arguments and 'kwargs' is for keyword arguments.'''
	#     super().save(*args, **kwargs)

	#     # Grab the image that was saved by opening
	# 		# the image of the current instance.
	#     img = Image.open(self.image.path)

	#     # If the height or the width of an image is
	# 		# greater than 300 pixels, then it will be
	# 		# resized.
	#     if img.height > 300 or img.width > 300:
	#					# Tuple of the max image sizes.
	#         output_size = (300, 300)
	#					
	#					# This will resize the image.
	#         img.thumbnail(output_size)
	#
	#         # Save the image back to the same path
	# 				# to overwrite the larger image.
	#         img.save(self.image.path)

# 22