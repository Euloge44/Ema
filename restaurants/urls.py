"""
URLs pour l'application restaurants.
"""
from django.urls import path

app_name = 'restaurants'

urlpatterns = [
    # URLs temporaires pour la Phase 1
    path('', lambda request: None, name='restaurants_list'),
]