from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# The "UserRegisterForm" class will be
# inheriting from the "UserCreationForm".


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=254, label="Email")

	class Meta:
		# Specify the model that this
		# form will interact with.
		model = User

		# Add the fields that will
		# be shown on the form.
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(max_length=254, label="Email")

	class Meta:
		model = User

		# The "UserUpdateForm" will allow the
		# username and email to be updated.
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		# The "ProfileUpdateForm" allows me to
		# update the 'image' and 'facial_image'
		# attributes of the 'Profile' class inside
		# django_project/users/forms.py.
		fields = ['m_Profile_Image', 'm_Facial_Image']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['m_Profile_Image'].required = False
		self.fields['m_Facial_Image'].required = False

	def clean(self):
		cleaned_data = super().clean()
		image = cleaned_data.get('m_Profile_Image')
		facial_image = cleaned_data.get('m_Facial_Image')

		if not image and not facial_image:
			raise forms.ValidationError(
				"Please upload either a Profile Image or a Facial Image."
			)

		return cleaned_data

# After adding a form in the "users/forms.py"
# file, I had to import it in the
# "users/views.py" file.

# 21