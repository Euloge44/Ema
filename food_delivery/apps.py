"""
Configuration de l'application principale food_delivery.
"""
from django.apps import AppConfig


class FoodDeliveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food_delivery'
    
    def ready(self):
        """Configuration à l'initialisation de l'application."""
        import food_delivery.signals