"""
URL patterns for the library search app.
"""
from django.urls import path
from . import views

app_name = 'library'


urlpatterns = [
       path('', views.home, name='home'),
     #  path('search', views.search, name='search'),
       path('sidebar', views.sidebar, name='sidebar'),
       path('api/search', views.api_search, name='api_search'),
]
