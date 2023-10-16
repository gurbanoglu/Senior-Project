from django.urls import path
from . import views

urlpatterns = [
    path('search-weather/', views.SearchWeather,
         name='search-weather'),
]

# 5
