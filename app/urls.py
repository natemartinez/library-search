"""
URL patterns for the library search app.
"""
from django.urls import path
from . import views

app_name = 'library'

# TODO(human): Define URL patterns for your library search
# Hint: You'll need at least:
# 1. A home page (use views.home)
# 2. A search results page (use views.search)
# Example pattern: path('', views.home, name='home')
# The 'name' parameter lets you reference URLs in templates with {% url 'library:home' %}

urlpatterns = [
       path('', views.home, name='home'),
       path('search', views.search, name='search') 
]
