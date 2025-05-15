from django.db import models
from django.contrib.auth.models import User

# Importing "Image" aides in resizing images.
from PIL import Image

# DEFAULT_PROFILE_IMAGE_URL = 'https://res.cloudinary.com/dybmcxawv/image/upload/v1747033011/profile_images/default_profile_image.png'

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
		User,
		on_delete=models.CASCADE,
		verbose_name="User"
	)

	# 'profile_images' will be the directory
	# where images get saved when a profile
	# image is uploaded.
	m_Profile_Image = models.ImageField(
    upload_to='profile_images/',
    verbose_name="Profile Image"
	)

	m_Profile_Image_URL = models.URLField(
		default='https://res.cloudinary.com/dybmcxawv/image/upload/v1747033011/profile_images/default_profile_image.png',
		max_length=500,
		verbose_name='Profile Image URL'
	)

	m_Facial_Image = models.ImageField(
		upload_to='facial_images/',
    verbose_name="Facial Image"
	)

	m_Facial_Image_URL = models.URLField(
		default='https://res.cloudinary.com/dybmcxawv/image/upload/v1747068277/facial_images/default_facial_image.jpg',
		max_length=500,
		verbose_name='Facial Image URL'
	)

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
	def save(self, *args, **kwargs):
		if self.m_Profile_Image:
			try:
				self.m_Profile_Image_URL = self.m_Profile_Image.url
			except ValueError:
				# Handle case where image is not
				# yet uploaded or invalid.
				pass

		if self.m_Facial_Image:
			try:
				self.m_Facial_Image_URL = self.m_Facial_Image.url
			except ValueError:
				# Handle case where image is not
				# yet uploaded or invalid.
				pass

		'''
	  This will execute the "save()" method of
	 	the parent class. The save() method must
		accept arguments that the parent class
	  might be expecting. 'args' is for positional
		arguments and 'kwargs' is for keyword arguments.'''
		super().save(*args, **kwargs)

	  # Grab the image that was saved by opening
		# the image of the current instance.
		# img = Image.open(self.image.path)

	  # If the height or the width of an image is
		# greater than 300 pixels, then it will be
		# resized.
		# if img.height > 300 or img.width > 300:
			# Tuple of the max image sizes.
			# output_size = (300, 300)

			# This will resize the image.
			# img.thumbnail(output_size)

	    # Save the image back to the same path
			# to overwrite the larger image.
			# img.save(self.image.path)

# 22