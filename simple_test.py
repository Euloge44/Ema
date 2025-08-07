#!/usr/bin/env python3
"""
Test simple de l'API.
"""
import requests
import json

def test_endpoint(url, method='GET', data=None):
    """Tester un endpoint."""
    print(f"\n🔍 Test: {method} {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers, timeout=5)
        
        print(f"📊 Statut: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Succès!")
            try:
                print(f"📄 JSON: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"📄 Texte: {response.text[:200]}")
        else:
            print(f"❌ Erreur {response.status_code}")
            print(f"📄 Contenu: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Test principal."""
    base = "http://localhost:8000"
    
    print("🚀 Test simple de l'API")
    print("=" * 40)
    
    # Test de la page d'accueil
    test_endpoint(f"{base}/")
    
    # Test de health check
    test_endpoint(f"{base}/health/")
    
    # Test de l'admin
    test_endpoint(f"{base}/admin/")
    
    # Test de la documentation
    test_endpoint(f"{base}/api/docs/")

if __name__ == "__main__":
    main()