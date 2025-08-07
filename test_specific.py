#!/usr/bin/env python3
"""
Script pour tester une URL spécifique et voir l'erreur exacte.
"""
import requests
import json

def test_url(url, method='GET', data=None):
    """Tester une URL spécifique."""
    print(f"\n🔍 Test de {method} {url}")
    print("=" * 50)
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            print(f"❌ Méthode {method} non supportée")
            return
        
        print(f"📊 Statut: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Succès!")
            if 'application/json' in response.headers.get('content-type', ''):
                try:
                    print(f"📄 Contenu JSON: {json.dumps(response.json(), indent=2)}")
                except:
                    print(f"📄 Contenu: {response.text[:500]}")
            else:
                print(f"📄 Contenu: {response.text[:500]}")
        else:
            print(f"❌ Erreur {response.status_code}")
            print(f"📄 Contenu d'erreur: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
    except requests.exceptions.Timeout:
        print("❌ Timeout")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale."""
    base_url = "http://localhost:8000"
    
    print("🚀 Test de URLs spécifiques")
    print("=" * 60)
    
    # Test des URLs principales
    urls_to_test = [
        ('/', 'GET'),
        ('/admin/', 'GET'),
        ('/api/docs/', 'GET'),
        ('/api/schema/', 'GET'),
        ('/api/auth/login/', 'POST', {
            'email': 'test@example.com',
            'password': 'testpass'
        }),
        ('/api/auth/register/', 'POST', {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'client',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }),
    ]
    
    for url, method, *args in urls_to_test:
        data = args[0] if args else None
        test_url(f"{base_url}{url}", method, data)

if __name__ == "__main__":
    main()