# The URL patterns for navigating throughout the "base" application are defined here.

from django.urls import path
from . import views

urlpatterns = [
    path('lobby/', views.Lobby, name='lobby'),
    path('room/', views.Room),
    path('get_token/', views.GetToken),
    path('create_member/', views.CreateMember),
    path('get_member/', views.GetMember),
    path('delete_member/', views.DeleteMember),
]

# 9
