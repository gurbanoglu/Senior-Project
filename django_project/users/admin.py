from django.contrib import admin
from .models import Profile

# Register "Profile" in users/admin.py,
# so that the user profiles can be seen
# on the admin page of the website.
admin.site.register(Profile)

# 4