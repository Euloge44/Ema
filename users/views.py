"""
Vues pour l'API des utilisateurs.
"""
from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, UserProfile, ClientProfile, RestaurantProfile, DeliveryProfile, AdminProfile
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserUpdateSerializer,
    CustomTokenObtainPairSerializer, PasswordChangeSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    LocationUpdateSerializer, UserSearchSerializer,
    UserProfileSerializer, ClientProfileSerializer, RestaurantProfileSerializer,
    DeliveryProfileSerializer, AdminProfileSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vue personnalisée pour l'obtention de tokens JWT."""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Vue pour l'inscription d'utilisateurs."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Créer un utilisateur avec gestion d'erreurs."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': _('Utilisateur créé avec succès.'),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour le profil utilisateur."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retourner l'utilisateur connecté."""
        return self.request.user


class UserListView(generics.ListAPIView):
    """Vue pour la liste des utilisateurs (admin seulement)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type', 'is_active', 'is_verified', 'city']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login', 'email']
    ordering = ['-date_joined']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour les détails d'un utilisateur (admin seulement)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class PasswordChangeView(APIView):
    """Vue pour le changement de mot de passe."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Changer le mot de passe de l'utilisateur connecté."""
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': _('Ancien mot de passe incorrect.')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': _('Mot de passe modifié avec succès.')
        }, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    """Vue pour la réinitialisation de mot de passe."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Demander une réinitialisation de mot de passe."""
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Ici, vous pouvez envoyer un email avec un token de réinitialisation
            # Pour l'instant, on simule juste la réponse
            return Response({
                'message': _('Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.')
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Pour des raisons de sécurité, on ne révèle pas si l'email existe
            return Response({
                'message': _('Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.')
            }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """Vue pour la confirmation de réinitialisation de mot de passe."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Confirmer la réinitialisation de mot de passe."""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ici, vous devriez valider le token et réinitialiser le mot de passe
        # Pour l'instant, on simule juste la réponse
        return Response({
            'message': _('Mot de passe réinitialisé avec succès.')
        }, status=status.HTTP_200_OK)


class LocationUpdateView(APIView):
    """Vue pour la mise à jour de localisation."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Mettre à jour la localisation de l'utilisateur."""
        serializer = LocationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_location(
            serializer.validated_data['latitude'],
            serializer.validated_data['longitude']
        )
        user.save()
        
        return Response({
            'message': _('Localisation mise à jour avec succès.')
        }, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    """Vue pour la recherche d'utilisateurs."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type', 'is_active', 'city']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Filtrer les utilisateurs selon les paramètres de recherche."""
        queryset = User.objects.all()
        
        # Filtres personnalisés
        query = self.request.query_params.get('query', None)
        if query:
            queryset = queryset.filter(
                Q(email__icontains=query) |
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        
        return queryset


class UserProfileUpdateView(generics.UpdateAPIView):
    """Vue pour la mise à jour du profil utilisateur."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retourner le profil de l'utilisateur connecté."""
        return self.request.user.profile


class ClientProfileUpdateView(generics.UpdateAPIView):
    """Vue pour la mise à jour du profil client."""
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retourner le profil client de l'utilisateur connecté."""
        if not self.request.user.is_client:
            raise permissions.PermissionDenied(_('Accès réservé aux clients.'))
        return self.request.user.client_profile


class RestaurantProfileUpdateView(generics.UpdateAPIView):
    """Vue pour la mise à jour du profil restaurant."""
    serializer_class = RestaurantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retourner le profil restaurant de l'utilisateur connecté."""
        if not self.request.user.is_restaurant:
            raise permissions.PermissionDenied(_('Accès réservé aux restaurants.'))
        return self.request.user.restaurant_profile


class DeliveryProfileUpdateView(generics.UpdateAPIView):
    """Vue pour la mise à jour du profil livreur."""
    serializer_class = DeliveryProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retourner le profil livreur de l'utilisateur connecté."""
        if not self.request.user.is_delivery:
            raise permissions.PermissionDenied(_('Accès réservé aux livreurs.'))
        return self.request.user.delivery_profile


class AdminProfileUpdateView(generics.UpdateAPIView):
    """Vue pour la mise à jour du profil administrateur."""
    serializer_class = AdminProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_object(self):
        """Retourner le profil admin de l'utilisateur connecté."""
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied(_('Accès réservé aux administrateurs.'))
        return self.request.user.admin_profile


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Vue pour la déconnexion."""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': _('Déconnexion réussie.')
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': _('Erreur lors de la déconnexion.')
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats_view(request):
    """Vue pour les statistiques de l'utilisateur."""
    user = request.user
    
    stats = {
        'user_type': user.user_type,
        'is_verified': user.is_verified,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    
    # Ajouter des statistiques spécifiques selon le type d'utilisateur
    if user.is_client:
        stats.update({
            'total_orders': 0,  # À implémenter avec l'app orders
            'favorite_restaurants_count': user.client_profile.favorite_restaurants.count(),
        })
    elif user.is_restaurant:
        stats.update({
            'total_orders': 0,  # À implémenter avec l'app orders
            'average_rating': user.restaurant_profile.average_rating,
            'total_reviews': user.restaurant_profile.total_reviews,
        })
    elif user.is_delivery:
        stats.update({
            'total_deliveries': user.delivery_profile.total_deliveries,
            'average_rating': user.delivery_profile.average_rating,
            'total_earnings': user.delivery_profile.total_earnings,
        })
    
    return Response(stats, status=status.HTTP_200_OK)