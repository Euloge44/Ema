"""
Signaux pour l'application users.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Créer automatiquement le profil utilisateur lors de la création d'un utilisateur."""
    if created:
        from .models import UserProfile, ClientProfile, RestaurantProfile, DeliveryProfile, AdminProfile
        
        # Créer le profil utilisateur de base
        UserProfile.objects.get_or_create(user=instance)
        
        # Créer le profil spécifique selon le type d'utilisateur
        if instance.user_type == 'client':
            ClientProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'restaurant':
            RestaurantProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'delivery':
            DeliveryProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'admin':
            AdminProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarder le profil utilisateur lors de la mise à jour."""
    try:
        instance.profile.save()
    except:
        pass