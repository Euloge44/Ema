"""
URLs pour l'application payments.
"""
from django.urls import path

app_name = 'payments'

urlpatterns = [
    # URLs temporaires pour la Phase 1
    path('', lambda request: None, name='payments_list'),
]