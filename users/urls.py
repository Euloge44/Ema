"""
URLs pour l'application users.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'

urlpatterns = [
    # Authentification
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profil utilisateur
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    
    # Profils spécifiques
    path('profile/client/', views.ClientProfileUpdateView.as_view(), name='client_profile'),
    path('profile/restaurant/', views.RestaurantProfileUpdateView.as_view(), name='restaurant_profile'),
    path('profile/delivery/', views.DeliveryProfileUpdateView.as_view(), name='delivery_profile'),
    path('profile/admin/', views.AdminProfileUpdateView.as_view(), name='admin_profile'),
    
    # Gestion des mots de passe
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Localisation
    path('location/update/', views.LocationUpdateView.as_view(), name='location_update'),
    
    # Statistiques
    path('stats/', views.user_stats_view, name='user_stats'),
    
    # Recherche (admin seulement)
    path('search/', views.UserSearchView.as_view(), name='user_search'),
    
    # Gestion des utilisateurs (admin seulement)
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]