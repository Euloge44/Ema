"""
Sérialiseurs pour l'API des utilisateurs.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, ClientProfile, RestaurantProfile, DeliveryProfile, AdminProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Sérialiseur personnalisé pour l'obtention de tokens JWT.
    """
    def validate(self, attrs):
        """Validation personnalisée avec gestion des erreurs."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError(_('Email ou mot de passe incorrect.'))
            if not user.is_active:
                raise serializers.ValidationError(_('Compte désactivé.'))
            
            refresh = self.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type,
                    'is_verified': user.is_verified,
                }
            }
            return data
        else:
            raise serializers.ValidationError(_('Email et mot de passe requis.'))


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil utilisateur."""
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'birth_date', 'email_notifications',
            'sms_notifications', 'push_notifications', 'profile_public',
            'show_location', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ClientProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil client."""
    
    class Meta:
        model = ClientProfile
        fields = [
            'dietary_restrictions', 'favorite_cuisines', 'saved_addresses',
            'default_payment_method', 'auto_tip_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class RestaurantProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil restaurant."""
    
    class Meta:
        model = RestaurantProfile
        fields = [
            'restaurant_name', 'description', 'cuisine_type', 'opening_hours',
            'is_open', 'delivery_radius', 'minimum_order', 'delivery_fee',
            'average_rating', 'total_reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['average_rating', 'total_reviews', 'created_at', 'updated_at']


class DeliveryProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil livreur."""
    
    class Meta:
        model = DeliveryProfile
        fields = [
            'vehicle_type', 'vehicle_plate', 'is_available', 'current_location',
            'last_location_update', 'total_deliveries', 'average_rating',
            'total_earnings', 'working_hours', 'preferred_zones',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total_deliveries', 'average_rating', 'total_earnings', 'created_at', 'updated_at']


class AdminProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil administrateur."""
    
    class Meta:
        model = AdminProfile
        fields = [
            'can_manage_users', 'can_manage_restaurants', 'can_manage_orders',
            'can_view_analytics', 'can_manage_payments', 'moderation_level',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur principal pour les utilisateurs."""
    profile = UserProfileSerializer(read_only=True)
    client_profile = ClientProfileSerializer(read_only=True)
    restaurant_profile = RestaurantProfileSerializer(read_only=True)
    delivery_profile = DeliveryProfileSerializer(read_only=True)
    admin_profile = AdminProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'phone_number',
            'user_type', 'location', 'address', 'city', 'postal_code',
            'is_verified', 'is_active', 'date_joined', 'last_login',
            'language', 'timezone', 'profile', 'client_profile',
            'restaurant_profile', 'delivery_profile', 'admin_profile',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Créer un utilisateur avec mot de passe hashé."""
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'inscription d'utilisateurs."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'phone_number',
            'user_type', 'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        """Validation des données d'inscription."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(_('Les mots de passe ne correspondent pas.'))
        return attrs
    
    def create(self, validated_data):
        """Créer un utilisateur avec profil approprié."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Créer le profil utilisateur de base
        UserProfile.objects.create(user=user)
        
        # Créer le profil spécifique selon le type d'utilisateur
        if user.user_type == 'client':
            ClientProfile.objects.create(user=user)
        elif user.user_type == 'restaurant':
            RestaurantProfile.objects.create(user=user)
        elif user.user_type == 'delivery':
            DeliveryProfile.objects.create(user=user)
        elif user.user_type == 'admin':
            AdminProfile.objects.create(user=user)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour d'utilisateurs."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'address', 'city',
            'postal_code', 'language', 'timezone'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Sérialiseur pour le changement de mot de passe."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validation du changement de mot de passe."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(_('Les nouveaux mots de passe ne correspondent pas.'))
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """Sérialiseur pour la réinitialisation de mot de passe."""
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Sérialiseur pour la confirmation de réinitialisation de mot de passe."""
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        """Validation de la confirmation de réinitialisation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(_('Les nouveaux mots de passe ne correspondent pas.'))
        return attrs


class LocationUpdateSerializer(serializers.Serializer):
    """Sérialiseur pour la mise à jour de localisation."""
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    
    def validate_latitude(self, value):
        """Validation de la latitude."""
        if not -90 <= value <= 90:
            raise serializers.ValidationError(_('Latitude invalide.'))
        return value
    
    def validate_longitude(self, value):
        """Validation de la longitude."""
        if not -180 <= value <= 180:
            raise serializers.ValidationError(_('Longitude invalide.'))
        return value


class UserSearchSerializer(serializers.Serializer):
    """Sérialiseur pour la recherche d'utilisateurs."""
    query = serializers.CharField(required=False)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, required=False)
    city = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)