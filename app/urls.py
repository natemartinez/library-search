"""
URL patterns for the library search app.
"""
from django.urls import path
from . import views

app_name = 'mind_lore'


urlpatterns = [
       path('', views.build_library, name='home'),
       path('acquisitions', views.acquisitions, name='acquisitions'),
       path('stacks', views.stacks, name='stacks'),
       path('the-desk', views.the_desk, name='the_desk'),
       path('storyboard', views.storyboard, name='storyboard'),
       path('relics', views.relics, name='relics'),
       path('sidebar', views.sidebar, name='sidebar'),
       path('api/search', views.api_search, name='api_search'),
]
