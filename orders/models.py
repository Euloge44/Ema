"""
Modèles pour la gestion des commandes.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

User = get_user_model()


class Order(models.Model):
    """
    Modèle pour les commandes.
    """
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('accepted', _('Acceptée')),
        ('preparing', _('En préparation')),
        ('ready', _('Prête')),
        ('picked_up', _('Récupérée')),
        ('delivered', _('Livrée')),
        ('cancelled', _('Annulée')),
    ]
    
    # Informations de base
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='orders')
    delivery_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    
    # Statut et suivi
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    status_updated_at = models.DateTimeField(_('dernière mise à jour du statut'), auto_now=True)
    
    # Adresse de livraison
    delivery_address = models.TextField(_('adresse de livraison'))
    delivery_city = models.CharField(_('ville de livraison'), max_length=100)
    delivery_phone = models.CharField(_('téléphone de livraison'), max_length=20)
    
    # Calculs
    subtotal = models.DecimalField(_('sous-total'), max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(_('frais de livraison'), max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(_('taxes'), max_digits=10, decimal_places=2, default=0)
    tip = models.DecimalField(_('pourboire'), max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2)
    
    # Notes et instructions
    special_instructions = models.TextField(_('instructions spéciales'), blank=True)
    estimated_delivery_time = models.DateTimeField(_('heure de livraison estimée'), null=True, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('commande')
        verbose_name_plural = _('commandes')
        db_table = 'orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['customer']),
            models.Index(fields=['restaurant']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Commande #{self.id} - {self.customer.get_full_name()}"


class OrderItem(models.Model):
    """
    Articles dans une commande.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('restaurants.MenuItem', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(_('quantité'), validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(_('prix unitaire'), max_digits=10, decimal_places=2)
    total_price = models.DecimalField(_('prix total'), max_digits=10, decimal_places=2)
    
    # Options personnalisées
    customizations = models.JSONField(_('personnalisations'), default=dict, blank=True)
    special_instructions = models.TextField(_('instructions spéciales'), blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('article de commande')
        verbose_name_plural = _('articles de commande')
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"


class OrderStatusHistory(models.Model):
    """
    Historique des changements de statut des commandes.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(_('statut'), max_length=20, choices=Order.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('historique de statut')
        verbose_name_plural = _('historiques de statut')
        db_table = 'order_status_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commande #{self.order.id} - {self.get_status_display()}"