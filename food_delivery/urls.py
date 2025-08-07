"""
URLs principales pour la plateforme de livraison de repas.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    path('health/', views.HealthCheckView.as_view(), name='health'),
    
    # Admin Django
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Applications
    path('api/auth/', include('users.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/delivery/', include('delivery.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications_app.urls')),
    path('api/analytics/', include('analytics.urls')),
]

# URLs pour les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)