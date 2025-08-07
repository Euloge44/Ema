"""
URLs pour l'application notifications.
"""
from django.urls import path

app_name = 'notifications_app'

urlpatterns = [
    # URLs temporaires pour la Phase 1
    path('', lambda request: None, name='notifications_list'),
]