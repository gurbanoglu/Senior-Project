from django.contrib import admin
from .models import MapDatabase, Video
from embed_video.admin import AdminVideoMixin


class AdminVideo(AdminVideoMixin, admin.ModelAdmin):
  pass

# The models for the "map_app" app are registered here.
admin.site.register(MapDatabase)
admin.site.register(Video, AdminVideo)

# 6