#!/usr/bin/env python3
"""
Script de test pour vérifier l'API de la plateforme de livraison de repas.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Tester les endpoints de l'API."""
    
    print("🧪 Test de l'API de la plateforme de livraison de repas")
    print("=" * 60)
    
    # Test 1: Vérifier que le serveur fonctionne
    print("\n1. Test de connectivité...")
    try:
        response = requests.get(f"{BASE_URL}/docs/")
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"❌ Serveur accessible mais statut: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
        return
    
    # Test 2: Documentation API
    print("\n2. Test de la documentation API...")
    try:
        response = requests.get(f"{BASE_URL}/schema/")
        if response.status_code == 200:
            print("✅ Documentation API accessible")
        else:
            print(f"❌ Documentation API: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur documentation API: {e}")
    
    # Test 3: Endpoints d'authentification
    print("\n3. Test des endpoints d'authentification...")
    
    # Test d'inscription
    registration_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "user_type": "client",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
        if response.status_code in [201, 400]:  # 400 si l'utilisateur existe déjà
            print("✅ Endpoint d'inscription accessible")
        else:
            print(f"❌ Endpoint d'inscription: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur inscription: {e}")
    
    # Test de connexion
    login_data = {
        "email": "admin@example.com",
        "password": "admin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✅ Endpoint de connexion accessible")
            # Sauvegarder le token pour les tests suivants
            token_data = response.json()
            if 'access' in token_data:
                print("✅ Token JWT généré avec succès")
                return token_data['access']
        else:
            print(f"❌ Endpoint de connexion: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
    
    return None

def test_authenticated_endpoints(token):
    """Tester les endpoints authentifiés."""
    if not token:
        print("❌ Pas de token disponible pour les tests authentifiés")
        return
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n4. Test des endpoints authentifiés...")
    
    # Test du profil utilisateur
    try:
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        if response.status_code == 200:
            print("✅ Endpoint profil utilisateur accessible")
            user_data = response.json()
            print(f"   Utilisateur: {user_data.get('first_name', '')} {user_data.get('last_name', '')}")
        else:
            print(f"❌ Endpoint profil: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur profil: {e}")
    
    # Test des statistiques utilisateur
    try:
        response = requests.get(f"{BASE_URL}/auth/stats/", headers=headers)
        if response.status_code == 200:
            print("✅ Endpoint statistiques accessible")
        else:
            print(f"❌ Endpoint statistiques: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")

def main():
    """Fonction principale."""
    print("🚀 Démarrage des tests de l'API...")
    
    # Tests de base
    token = test_api_endpoints()
    
    # Tests authentifiés
    if token:
        test_authenticated_endpoints(token)
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés !")
    print("\n📚 Documentation disponible sur: http://localhost:8000/api/docs/")
    print("🔧 Interface d'administration: http://localhost:8000/admin/")

if __name__ == "__main__":
    main()