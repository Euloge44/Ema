"""
Signaux globaux pour la plateforme de livraison de repas.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Créer automatiquement le profil utilisateur lors de la création d'un utilisateur."""
    if created:
        # La logique de création de profil sera dans l'app users
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarder le profil utilisateur lors de la mise à jour."""
    # La logique de sauvegarde sera dans l'app users
    pass