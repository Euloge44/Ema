"""
URLs pour l'application analytics.
"""
from django.urls import path

app_name = 'analytics'

urlpatterns = [
    # URLs temporaires pour la Phase 1
    path('', lambda request: None, name='analytics_list'),
]