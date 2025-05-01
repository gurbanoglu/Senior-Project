from django.db import models
from embed_video.fields import EmbedVideoField

# This file contains the definitions for
# the models of the "map_app" app.


class MapDatabase(models.Model):
  m_address = models.CharField(
    max_length=200, null=True, verbose_name="Address")

  m_date = models.DateTimeField(
    auto_now_add=True, verbose_name="Date")

  def __str__(self):
    return str(self.m_address)

  class Meta:
    verbose_name = "Map Database"
    verbose_name_plural = "Map Databases"


class Video(models.Model):
  m_title = models.CharField(
    max_length=100, verbose_name="Title")

  m_added = models.DateTimeField(
    auto_now_add=True, verbose_name="Added")

  m_url = EmbedVideoField(verbose_name="URL")

  def __str__(self):
    return str(self.m_title)

  # Display the uploaded videos in
  # the order of newest to oldest.
  class Meta:
    verbose_name = "Video"
    verbose_name_plural = "Videos"
    ordering = ['-m_added']

# 17