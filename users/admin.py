"""
Interface d'administration pour les utilisateurs.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile, ClientProfile, RestaurantProfile, DeliveryProfile, AdminProfile


class UserProfileInline(admin.StackedInline):
    """Inline pour le profil utilisateur."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profil utilisateur'


class ClientProfileInline(admin.StackedInline):
    """Inline pour le profil client."""
    model = ClientProfile
    can_delete = False
    verbose_name_plural = 'profil client'


class RestaurantProfileInline(admin.StackedInline):
    """Inline pour le profil restaurant."""
    model = RestaurantProfile
    can_delete = False
    verbose_name_plural = 'profil restaurant'


class DeliveryProfileInline(admin.StackedInline):
    """Inline pour le profil livreur."""
    model = DeliveryProfile
    can_delete = False
    verbose_name_plural = 'profil livreur'


class AdminProfileInline(admin.StackedInline):
    """Inline pour le profil administrateur."""
    model = AdminProfile
    can_delete = False
    verbose_name_plural = 'profil administrateur'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Interface d'administration pour les utilisateurs."""
    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_active', 'is_verified', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_verified', 'date_joined', 'city')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {'fields': ('username', 'first_name', 'last_name', 'phone_number')}),
        (_('Type et statut'), {'fields': ('user_type', 'is_active', 'is_verified', 'is_staff', 'is_superuser')}),
        (_('Géolocalisation'), {'fields': ('location', 'address', 'city', 'postal_code')}),
        (_('Préférences'), {'fields': ('language', 'timezone')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')}),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    
    def get_inlines(self, request, obj=None):
        """Retourner les inlines appropriés selon le type d'utilisateur."""
        inlines = [UserProfileInline]
        
        if obj and obj.user_type == 'client':
            inlines.append(ClientProfileInline)
        elif obj and obj.user_type == 'restaurant':
            inlines.append(RestaurantProfileInline)
        elif obj and obj.user_type == 'delivery':
            inlines.append(DeliveryProfileInline)
        elif obj and obj.user_type == 'admin':
            inlines.append(AdminProfileInline)
        
        return inlines


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les profils utilisateurs."""
    list_display = ('user', 'birth_date', 'email_notifications', 'sms_notifications', 'push_notifications')
    list_filter = ('email_notifications', 'sms_notifications', 'push_notifications', 'profile_public', 'show_location')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
    ordering = ('user__email',)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les profils clients."""
    list_display = ('user', 'auto_tip_percentage', 'default_payment_method')
    list_filter = ('auto_tip_percentage', 'default_payment_method')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
    ordering = ('user__email',)


@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les profils restaurants."""
    list_display = ('user', 'restaurant_name', 'cuisine_type', 'is_open', 'average_rating', 'total_reviews')
    list_filter = ('cuisine_type', 'is_open', 'average_rating', 'delivery_radius')
    search_fields = ('user__email', 'restaurant_name', 'cuisine_type')
    ordering = ('restaurant_name',)


@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les profils livreurs."""
    list_display = ('user', 'vehicle_type', 'is_available', 'total_deliveries', 'average_rating', 'total_earnings')
    list_filter = ('vehicle_type', 'is_available', 'average_rating')
    search_fields = ('user__email', 'user__username', 'vehicle_plate')
    ordering = ('user__email',)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    """Interface d'administration pour les profils administrateurs."""
    list_display = ('user', 'moderation_level', 'can_manage_users', 'can_manage_restaurants', 'can_view_analytics')
    list_filter = ('moderation_level', 'can_manage_users', 'can_manage_restaurants', 'can_manage_orders', 'can_view_analytics', 'can_manage_payments')
    search_fields = ('user__email', 'user__username')
    ordering = ('user__email',)