#!/usr/bin/env python3
"""
Script de diagnostic pour identifier les problèmes de configuration.
"""
import os
import sys
import django
from pathlib import Path

def check_django_setup():
    """Vérifier la configuration Django."""
    print("🔍 Diagnostic de la configuration Django")
    print("=" * 50)
    
    # Vérifier le répertoire de travail
    print(f"📁 Répertoire de travail: {os.getcwd()}")
    
    # Vérifier les fichiers essentiels
    essential_files = [
        'manage.py',
        'food_delivery/settings.py',
        'food_delivery/urls.py',
        'requirements.txt',
        '.env'
    ]
    
    print("\n📋 Vérification des fichiers essentiels:")
    for file in essential_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MANQUANT")
    
    # Vérifier les applications
    print("\n📱 Vérification des applications:")
    apps = [
        'users',
        'restaurants', 
        'orders',
        'delivery',
        'payments',
        'notifications_app',
        'analytics'
    ]
    
    for app in apps:
        if os.path.exists(app):
            print(f"  ✅ {app}")
        else:
            print(f"  ❌ {app} - MANQUANT")
    
    # Configuration Django
    print("\n⚙️ Configuration Django:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
        django.setup()
        print("  ✅ Django configuré avec succès")
        
        # Vérifier les applications installées
        from django.conf import settings
        print(f"  📊 Applications installées: {len(settings.INSTALLED_APPS)}")
        
        # Vérifier la base de données
        from django.db import connection
        connection.ensure_connection()
        print("  ✅ Connexion à la base de données OK")
        
    except Exception as e:
        print(f"  ❌ Erreur Django: {e}")
        return False
    
    return True

def check_dependencies():
    """Vérifier les dépendances."""
    print("\n📦 Vérification des dépendances:")
    
    required_packages = [
        'django',
        'djangorestframework',
        'djangorestframework_simplejwt',
        'django_cors_headers',
        'django_filters',
        'channels',
        'django_phonenumber_field',
        'django_extensions',
        'drf_spectacular',
        'django_axes',
        'django_redis',
        'Pillow'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MANQUANT")

def check_urls():
    """Vérifier les URLs."""
    print("\n🔗 Vérification des URLs:")
    
    try:
        from food_delivery.urls import urlpatterns
        
        print("  ✅ URLs configurées avec succès")
        
        # Lister les URLs principales
        print("  📋 URLs principales:")
        for pattern in urlpatterns:
            if hasattr(pattern, 'pattern'):
                print(f"    - {pattern.pattern}")
            elif hasattr(pattern, 'url_patterns'):
                print(f"    - {pattern.namespace} (include)")
        
    except Exception as e:
        print(f"  ❌ Erreur URLs: {e}")

def check_models():
    """Vérifier les modèles."""
    print("\n🗄️ Vérification des modèles:")
    
    try:
        from django.apps import apps
        
        models_to_check = [
            'users.User',
            'users.UserProfile',
            'users.ClientProfile',
            'restaurants.Restaurant',
            'restaurants.MenuItem',
            'orders.Order',
            'notifications_app.Notification'
        ]
        
        for model_name in models_to_check:
            try:
                app_label, model_name_short = model_name.split('.')
                model = apps.get_model(app_label, model_name_short)
                print(f"  ✅ {model_name}")
            except Exception as e:
                print(f"  ❌ {model_name}: {e}")
                
    except Exception as e:
        print(f"  ❌ Erreur modèles: {e}")

def main():
    """Fonction principale."""
    print("🚀 Diagnostic de la plateforme de livraison de repas")
    print("=" * 60)
    
    # Vérifications
    django_ok = check_dependencies()
    check_django_setup()
    check_urls()
    check_models()
    
    print("\n" + "=" * 60)
    print("✅ Diagnostic terminé !")
    
    if django_ok:
        print("\n🎉 Configuration valide !")
        print("Vous pouvez maintenant lancer le serveur avec:")
        print("python manage.py runserver")
    else:
        print("\n⚠️ Problèmes détectés.")
        print("Vérifiez les erreurs ci-dessus et corrigez-les.")

if __name__ == "__main__":
    main()