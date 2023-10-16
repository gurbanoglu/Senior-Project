from django.db import models
# This will be a date time that takes the time zone settings into consideration.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Models for the "blog" application.

# Create a model called "Post".
# The "Post" class will inherit from models.model.
# Each class is going to be its own table in the database.
# Each attribute in the "Post" class will be a different field within the database.


class Post(models.Model):
    # Each title in the database can be up to 100 characters.
    m_title = models.CharField(max_length=100, verbose_name="Title")
    # The TextField() is unrestricted in terms of size.
    m_content = models.TextField(verbose_name="Content")
    # The date of each post will be set to the current date time only when the post is created.
    m_datePosted = models.DateTimeField(default=timezone.now, verbose_name="Date Posted")

    # The relationship between a user and a post is one to many because a user can have many posts.
    m_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    # Include "on_delete" because it tells django that if a user who created a post
    # gets deleted, then all of the posts that belong to that user will be deleted as well.

    def __str__(self):
        # This will make each post be printed out by the title.
        return self.m_title

    # Create a get absolute URL method, so that django knows how to
    # find the location of a specific post. The get_absolute_url()
    # function is a built-in function in Django.
    def get_absolute_url(self):
        # Return the full path or url to 'post-detail' route (a certain post) as a string
        # and let the view handle the redirect.
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

# 23
