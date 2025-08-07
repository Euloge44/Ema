"""
URLs pour l'application delivery.
"""
from django.urls import path

app_name = 'delivery'

urlpatterns = [
    # URLs temporaires pour la Phase 1
    path('', lambda request: None, name='delivery_list'),
]