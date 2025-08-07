"""
Modèles pour la gestion des utilisateurs multi-rôles.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.geos import Point


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec support multi-rôles.
    """
    USER_TYPE_CHOICES = [
        ('client', _('Client')),
        ('restaurant', _('Restaurant')),
        ('delivery', _('Livreur')),
        ('admin', _('Administrateur')),
    ]
    
    # Champs de base
    email = models.EmailField(_('adresse email'), unique=True)
    phone_number = PhoneNumberField(_('numéro de téléphone'), blank=True, null=True)
    user_type = models.CharField(_('type d\'utilisateur'), max_length=20, choices=USER_TYPE_CHOICES, default='client')
    
    # Géolocalisation
    # location = gis_models.PointField(_('localisation'), null=True, blank=True)
    address = models.TextField(_('adresse complète'), blank=True)
    city = models.CharField(_('ville'), max_length=100, blank=True)
    postal_code = models.CharField(_('code postal'), max_length=10, blank=True)
    
    # Statut et vérification
    is_verified = models.BooleanField(_('compte vérifié'), default=False)
    is_active = models.BooleanField(_('compte actif'), default=True)
    date_joined = models.DateTimeField(_('date d\'inscription'), auto_now_add=True)
    last_login = models.DateTimeField(_('dernière connexion'), auto_now=True)
    
    # Préférences
    language = models.CharField(_('langue'), max_length=10, default='fr')
    timezone = models.CharField(_('fuseau horaire'), max_length=50, default='Africa/Lome')
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def set_location(self, latitude, longitude):
        """Définir la localisation géographique."""
        # if latitude and longitude:
        #     self.location = Point(longitude, latitude, srid=4326)
        pass
    
    @property
    def is_client(self):
        """Vérifier si l'utilisateur est un client."""
        return self.user_type == 'client'
    
    @property
    def is_restaurant(self):
        """Vérifier si l'utilisateur est un restaurant."""
        return self.user_type == 'restaurant'
    
    @property
    def is_delivery(self):
        """Vérifier si l'utilisateur est un livreur."""
        return self.user_type == 'delivery'
    
    @property
    def is_admin(self):
        """Vérifier si l'utilisateur est un administrateur."""
        return self.user_type == 'admin'


class UserProfile(models.Model):
    """
    Profil étendu pour les utilisateurs.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Informations personnelles
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_('biographie'), blank=True)
    birth_date = models.DateField(_('date de naissance'), null=True, blank=True)
    
    # Préférences de notification
    email_notifications = models.BooleanField(_('notifications email'), default=True)
    sms_notifications = models.BooleanField(_('notifications SMS'), default=False)
    push_notifications = models.BooleanField(_('notifications push'), default=True)
    
    # Paramètres de confidentialité
    profile_public = models.BooleanField(_('profil public'), default=True)
    show_location = models.BooleanField(_('afficher localisation'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profil utilisateur')
        verbose_name_plural = _('profils utilisateurs')
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profil de {self.user.get_full_name()}"


class ClientProfile(models.Model):
    """
    Profil spécifique pour les clients.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    
    # Préférences alimentaires
    dietary_restrictions = models.JSONField(_('restrictions alimentaires'), default=dict, blank=True)
    favorite_cuisines = models.JSONField(_('cuisines préférées'), default=list, blank=True)
    
    # Historique et préférences
    # favorite_restaurants = models.ManyToManyField('restaurants.Restaurant', blank=True, related_name='favorited_by', through='ClientRestaurantFavorite')
    saved_addresses = models.JSONField(_('adresses sauvegardées'), default=list, blank=True)
    
    # Paramètres de commande
    default_payment_method = models.CharField(_('méthode de paiement par défaut'), max_length=50, blank=True)
    auto_tip_percentage = models.DecimalField(_('pourboire automatique (%)'), max_digits=5, decimal_places=2, default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profil client')
        verbose_name_plural = _('profils clients')
        db_table = 'client_profiles'
    
    def __str__(self):
        return f"Profil client de {self.user.get_full_name()}"


class RestaurantProfile(models.Model):
    """
    Profil spécifique pour les restaurants.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    
    # Informations du restaurant
    restaurant_name = models.CharField(_('nom du restaurant'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    cuisine_type = models.CharField(_('type de cuisine'), max_length=100)
    
    # Horaires et disponibilité
    opening_hours = models.JSONField(_('horaires d\'ouverture'), default=dict)
    is_open = models.BooleanField(_('ouvert'), default=True)
    
    # Paramètres de livraison
    delivery_radius = models.DecimalField(_('rayon de livraison (km)'), max_digits=5, decimal_places=2, default=5.0)
    minimum_order = models.DecimalField(_('commande minimum'), max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(_('frais de livraison'), max_digits=10, decimal_places=2, default=0)
    
    # Évaluations
    average_rating = models.DecimalField(_('note moyenne'), max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(_('nombre total d\'avis'), default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profil restaurant')
        verbose_name_plural = _('profils restaurants')
        db_table = 'restaurant_profiles'
    
    def __str__(self):
        return f"Restaurant: {self.restaurant_name}"


class DeliveryProfile(models.Model):
    """
    Profil spécifique pour les livreurs.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_profile')
    
    # Informations de livraison
    vehicle_type = models.CharField(_('type de véhicule'), max_length=50, choices=[
        ('bike', _('Vélo')),
        ('motorcycle', _('Moto')),
        ('car', _('Voiture')),
        ('scooter', _('Scooter')),
    ])
    vehicle_plate = models.CharField(_('plaque d\'immatriculation'), max_length=20, blank=True)
    
    # Statut de livraison
    is_available = models.BooleanField(_('disponible'), default=True)
    # current_location = gis_models.PointField(_('localisation actuelle'), null=True, blank=True)
    last_location_update = models.DateTimeField(_('dernière mise à jour de localisation'), null=True, blank=True)
    
    # Performance
    total_deliveries = models.PositiveIntegerField(_('total des livraisons'), default=0)
    average_rating = models.DecimalField(_('note moyenne'), max_digits=3, decimal_places=2, default=0)
    total_earnings = models.DecimalField(_('gains totaux'), max_digits=10, decimal_places=2, default=0)
    
    # Paramètres de travail
    working_hours = models.JSONField(_('heures de travail'), default=dict)
    preferred_zones = models.JSONField(_('zones préférées'), default=list, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profil livreur')
        verbose_name_plural = _('profils livreurs')
        db_table = 'delivery_profiles'
    
    def __str__(self):
        return f"Livreur: {self.user.get_full_name()}"


class AdminProfile(models.Model):
    """
    Profil spécifique pour les administrateurs.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    
    # Permissions administratives
    can_manage_users = models.BooleanField(_('gérer les utilisateurs'), default=False)
    can_manage_restaurants = models.BooleanField(_('gérer les restaurants'), default=False)
    can_manage_orders = models.BooleanField(_('gérer les commandes'), default=False)
    can_view_analytics = models.BooleanField(_('voir les analytics'), default=False)
    can_manage_payments = models.BooleanField(_('gérer les paiements'), default=False)
    
    # Paramètres de modération
    moderation_level = models.CharField(_('niveau de modération'), max_length=20, choices=[
        ('basic', _('Basique')),
        ('advanced', _('Avancé')),
        ('super', _('Super')),
    ], default='basic')
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profil administrateur')
        verbose_name_plural = _('profils administrateurs')
        db_table = 'admin_profiles'
    
    def __str__(self):
        return f"Admin: {self.user.get_full_name()}"


# class ClientRestaurantFavorite(models.Model):
#     """
#     Modèle de liaison pour les restaurants favoris des clients.
#     """
#     client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
#     restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     
#     class Meta:
#         unique_together = ['client', 'restaurant']
#         db_table = 'client_restaurant_favorites'
#     
#     def __str__(self):
#         return f"{self.client.user.get_full_name()} - {self.restaurant.name}"