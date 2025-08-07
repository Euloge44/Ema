"""
URLs pour l'application orders.
"""
from django.urls import path

app_name = 'orders'

urlpatterns = [
    # URLs temporaires pour la Phase 1
    path('', lambda request: None, name='orders_list'),
]