from django.contrib import admin
from .models import RoomMember

# The "RoomMember" model inside the 'base'
# application is being registered here.
admin.site.register(RoomMember)

# 4