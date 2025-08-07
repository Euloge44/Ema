"""
Modèles pour le système de notifications.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Notification(models.Model):
    """
    Modèle pour les notifications utilisateur.
    """
    NOTIFICATION_TYPES = [
        ('order_status', _('Statut de commande')),
        ('delivery_update', _('Mise à jour de livraison')),
        ('payment', _('Paiement')),
        ('promotion', _('Promotion')),
        ('system', _('Système')),
    ]
    
    # Destinataire
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Type et contenu
    notification_type = models.CharField(_('type'), max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(_('titre'), max_length=255)
    message = models.TextField(_('message'))
    
    # Référence à un objet (optionnel)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Données supplémentaires
    data = models.JSONField(_('données supplémentaires'), default=dict, blank=True)
    
    # Statut
    is_read = models.BooleanField(_('lu'), default=False)
    is_sent = models.BooleanField(_('envoyé'), default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Notification pour {self.recipient.get_full_name()}: {self.title}"
    
    def mark_as_read(self):
        """Marquer la notification comme lue."""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class NotificationTemplate(models.Model):
    """
    Modèles de notifications réutilisables.
    """
    name = models.CharField(_('nom'), max_length=100, unique=True)
    notification_type = models.CharField(_('type'), max_length=20, choices=Notification.NOTIFICATION_TYPES)
    title_template = models.CharField(_('modèle de titre'), max_length=255)
    message_template = models.TextField(_('modèle de message'))
    is_active = models.BooleanField(_('actif'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('modèle de notification')
        verbose_name_plural = _('modèles de notifications')
        db_table = 'notification_templates'
    
    def __str__(self):
        return self.name
    
    def render(self, context):
        """Rendre le template avec le contexte fourni."""
        from django.template import Template, Context
        title = Template(self.title_template).render(Context(context))
        message = Template(self.message_template).render(Context(context))
        return title, message


class NotificationPreference(models.Model):
    """
    Préférences de notification par utilisateur.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Types de notifications
    email_notifications = models.BooleanField(_('notifications email'), default=True)
    sms_notifications = models.BooleanField(_('notifications SMS'), default=False)
    push_notifications = models.BooleanField(_('notifications push'), default=True)
    in_app_notifications = models.BooleanField(_('notifications dans l\'app'), default=True)
    
    # Préférences par type
    order_status_notifications = models.BooleanField(_('notifications statut commande'), default=True)
    delivery_update_notifications = models.BooleanField(_('notifications livraison'), default=True)
    payment_notifications = models.BooleanField(_('notifications paiement'), default=True)
    promotion_notifications = models.BooleanField(_('notifications promotion'), default=True)
    system_notifications = models.BooleanField(_('notifications système'), default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('préférence de notification')
        verbose_name_plural = _('préférences de notifications')
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"Préférences de {self.user.get_full_name()}"