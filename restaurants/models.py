"""
Modèles pour la gestion des restaurants et menus.
"""
from django.db import models
# from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class CuisineType(models.Model):
    """
    Types de cuisine disponibles.
    """
    name = models.CharField(_('nom'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icône'), max_length=50, blank=True)
    is_active = models.BooleanField(_('actif'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('type de cuisine')
        verbose_name_plural = _('types de cuisine')
        db_table = 'cuisine_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    """
    Modèle pour les restaurants.
    """
    # Informations de base
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_restaurants')
    name = models.CharField(_('nom'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    cuisine_type = models.ForeignKey(CuisineType, on_delete=models.PROTECT, related_name='restaurants')
    
    # Géolocalisation
    # location = gis_models.PointField(_('localisation'), null=True, blank=True)
    address = models.TextField(_('adresse complète'))
    city = models.CharField(_('ville'), max_length=100)
    postal_code = models.CharField(_('code postal'), max_length=10, blank=True)
    
    # Contact
    phone_number = models.CharField(_('numéro de téléphone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('site web'), blank=True)
    
    # Horaires et disponibilité
    opening_hours = models.JSONField(_('horaires d\'ouverture'), default=dict)
    is_open = models.BooleanField(_('ouvert'), default=True)
    is_verified = models.BooleanField(_('vérifié'), default=False)
    
    # Paramètres de livraison
    delivery_radius = models.DecimalField(_('rayon de livraison (km)'), max_digits=5, decimal_places=2, default=5.0)
    minimum_order = models.DecimalField(_('commande minimum'), max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(_('frais de livraison'), max_digits=10, decimal_places=2, default=0)
    preparation_time = models.PositiveIntegerField(_('temps de préparation (minutes)'), default=30)
    
    # Évaluations et statistiques
    average_rating = models.DecimalField(_('note moyenne'), max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(_('nombre total d\'avis'), default=0)
    total_orders = models.PositiveIntegerField(_('nombre total de commandes'), default=0)
    
    # Images
    logo = models.ImageField(_('logo'), upload_to='restaurants/logos/', blank=True, null=True)
    cover_image = models.ImageField(_('image de couverture'), upload_to='restaurants/covers/', blank=True, null=True)
    
    # Statut
    is_active = models.BooleanField(_('actif'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('restaurant')
        verbose_name_plural = _('restaurants')
        db_table = 'restaurants'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_open']),
            models.Index(fields=['average_rating']),
        ]
    
    def __str__(self):
        return self.name
    
    def set_location(self, latitude, longitude):
        """Définir la localisation géographique."""
        # if latitude and longitude:
        #     self.location = Point(longitude, latitude, srid=4326)
        pass
    
    @property
    def is_available_for_delivery(self):
        """Vérifier si le restaurant est disponible pour la livraison."""
        return self.is_active and self.is_open and self.is_verified


class Category(models.Model):
    """
    Catégories de plats dans un restaurant.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(_('nom'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(_('ordre'), default=0)
    is_active = models.BooleanField(_('actif'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('catégorie')
        verbose_name_plural = _('catégories')
        db_table = 'categories'
        ordering = ['order', 'name']
        unique_together = ['restaurant', 'name']
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class MenuItem(models.Model):
    """
    Plats dans le menu d'un restaurant.
    """
    # Informations de base
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(_('nom'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    
    # Prix et disponibilité
    price = models.DecimalField(_('prix'), max_digits=10, decimal_places=2)
    is_available = models.BooleanField(_('disponible'), default=True)
    is_featured = models.BooleanField(_('mis en avant'), default=False)
    
    # Images
    image = models.ImageField(_('image'), upload_to='menu_items/', blank=True, null=True)
    
    # Informations nutritionnelles
    calories = models.PositiveIntegerField(_('calories'), blank=True, null=True)
    allergens = models.JSONField(_('allergènes'), default=list, blank=True)
    dietary_tags = models.JSONField(_('tags alimentaires'), default=list, blank=True)
    
    # Préparation
    preparation_time = models.PositiveIntegerField(_('temps de préparation (minutes)'), default=15)
    
    # Évaluations
    average_rating = models.DecimalField(_('note moyenne'), max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(_('nombre total d\'avis'), default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('plat')
        verbose_name_plural = _('plats')
        db_table = 'menu_items'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_available']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class MenuItemOption(models.Model):
    """
    Options personnalisables pour les plats (ex: taille, extras).
    """
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(_('nom'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    price_modifier = models.DecimalField(_('modificateur de prix'), max_digits=10, decimal_places=2, default=0)
    is_required = models.BooleanField(_('obligatoire'), default=False)
    max_selections = models.PositiveIntegerField(_('sélections maximum'), default=1)
    order = models.PositiveIntegerField(_('ordre'), default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('option de plat')
        verbose_name_plural = _('options de plats')
        db_table = 'menu_item_options'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"


class MenuItemOptionChoice(models.Model):
    """
    Choix disponibles pour une option de plat.
    """
    option = models.ForeignKey(MenuItemOption, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(_('nom'), max_length=100)
    price_modifier = models.DecimalField(_('modificateur de prix'), max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(_('disponible'), default=True)
    order = models.PositiveIntegerField(_('ordre'), default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('choix d\'option')
        verbose_name_plural = _('choix d\'options')
        db_table = 'menu_item_option_choices'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.option.name} - {self.name}"


class Review(models.Model):
    """
    Avis des clients sur les restaurants.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_reviews')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    
    # Évaluation
    rating = models.PositiveIntegerField(_('note'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(_('commentaire'), blank=True)
    
    # Photos
    photos = models.JSONField(_('photos'), default=list, blank=True)
    
    # Statut
    is_verified = models.BooleanField(_('vérifié'), default=False)
    is_public = models.BooleanField(_('public'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('avis')
        verbose_name_plural = _('avis')
        db_table = 'reviews'
        unique_together = ['restaurant', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Avis de {self.user.get_full_name()} sur {self.restaurant.name}"


class Promotion(models.Model):
    """
    Promotions et offres spéciales des restaurants.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='promotions')
    name = models.CharField(_('nom'), max_length=200)
    description = models.TextField(_('description'))
    
    # Type de promotion
    PROMOTION_TYPES = [
        ('percentage', _('Pourcentage')),
        ('fixed_amount', _('Montant fixe')),
        ('free_delivery', _('Livraison gratuite')),
        ('buy_one_get_one', _('Achetez un, obtenez un gratuit')),
    ]
    promotion_type = models.CharField(_('type de promotion'), max_length=20, choices=PROMOTION_TYPES)
    discount_value = models.DecimalField(_('valeur de la réduction'), max_digits=10, decimal_places=2)
    
    # Conditions
    minimum_order = models.DecimalField(_('commande minimum'), max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(_('réduction maximum'), max_digits=10, decimal_places=2, blank=True, null=True)
    applicable_items = models.ManyToManyField(MenuItem, blank=True, related_name='promotions')
    
    # Dates
    start_date = models.DateTimeField(_('date de début'))
    end_date = models.DateTimeField(_('date de fin'))
    
    # Utilisation
    max_uses = models.PositiveIntegerField(_('utilisations maximum'), blank=True, null=True)
    current_uses = models.PositiveIntegerField(_('utilisations actuelles'), default=0)
    
    # Statut
    is_active = models.BooleanField(_('actif'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')
        db_table = 'promotions'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"
    
    @property
    def is_valid(self):
        """Vérifier si la promotion est valide."""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )