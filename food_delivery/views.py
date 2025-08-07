"""
Vues principales pour la plateforme de livraison de repas.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View


def home(request):
    """
    Page d'accueil de la plateforme.
    """
    return JsonResponse({
        'message': 'Bienvenue sur la plateforme de livraison de repas',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'auth': '/api/auth/',
            'restaurants': '/api/restaurants/',
            'orders': '/api/orders/',
            'delivery': '/api/delivery/',
            'payments': '/api/payments/',
            'notifications': '/api/notifications/',
            'analytics': '/api/analytics/',
        }
    })


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(View):
    """
    Vue pour vérifier l'état de santé de l'API.
    """
    
    def get(self, request):
        """Vérification de santé de l'API."""
        return JsonResponse({
            'status': 'healthy',
            'message': 'API fonctionnelle',
            'version': '1.0.0'
        })
    
    def post(self, request):
        """Test POST pour l'API."""
        return JsonResponse({
            'status': 'success',
            'message': 'Test POST réussi',
            'data': request.POST.dict() if request.POST else {}
        })