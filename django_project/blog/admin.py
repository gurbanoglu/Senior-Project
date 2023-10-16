from django.contrib import admin

# Import the "Post" class.
from .models import Post

# This is where we will register our models, so that they can appear on the admin page.
# This is the backend admin view.

# Register the "Post" model.
admin.site.register(Post)

# 3
