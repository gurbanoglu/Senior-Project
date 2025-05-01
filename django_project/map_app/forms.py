from django import forms

'''
I imported the "MapDatabase" model from
the map_app/models.py file because below
I am created a form class for that
particular model.'''
from .models import MapDatabase

# Django ModelForm is used subsequently to
# convert a model into a Django form class
# in this file.


class MapDataForm(forms.ModelForm):
	m_address = forms.CharField(label='Enter Location: ')

	# The "Meta" class has information regarding
	# the class that is of interest.
	class Meta:
		'''
		'MapDataForm' is being created for the
		'MapDatabase' model. By assigning
		"MapDatabase" to "model", I am telling
		Django which model this form class should
		be based on.'''
		model = MapDatabase

		# Here it is indicated that I am interested
		# in the 'address' field of the "MapDatabase"
		# model.
		fields = ['m_address', ]

# 13