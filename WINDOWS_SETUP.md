# 🪟 Guide d'Installation Windows

## ✅ Problème Résolu

Le problème que vous rencontriez était dû à l'incompatibilité entre `django-notifications-hq` et Django 4.2+ avec Python 3.13. J'ai créé un système de notifications personnalisé et compatible.

## 🚀 Installation Rapide

### 1. Prérequis
```bash
# Vérifier Python
python --version  # Doit être 3.11+

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate
```

### 2. Installer les Dépendances
```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration
```bash
# Copier le fichier d'environnement
copy .env.example .env

# Éditer .env avec vos paramètres
# (utilisez Notepad ou votre éditeur préféré)
```

### 4. Base de Données
```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### 5. Lancer le Serveur
```bash
python manage.py runserver
```

## 🔧 Résolution des Problèmes Courants

### Erreur : `index_together`
**Problème** : `TypeError: 'class Meta' got invalid attribute(s): index_together`

**Solution** : ✅ **Résolu** - J'ai remplacé `django-notifications-hq` par un système personnalisé compatible.

### Erreur : `ModuleNotFoundError`
**Problème** : `No module named 'django_redis'`

**Solution** :
```bash
pip install django-redis
```

### Erreur : `psycopg2`
**Problème** : Erreur lors de l'installation de psycopg2

**Solution** :
```bash
# Utiliser la version binaire
pip install psycopg2-binary
```

### Erreur : `GDAL`
**Problème** : Erreur lors de l'installation de GDAL pour PostGIS

**Solution** :
```bash
# Pour le développement, utiliser SQLite (déjà configuré)
# Pour la production, installer GDAL via conda ou OSGeo4W
```

## 📁 Structure du Projet

```
food-delivery-platform/
├── food_delivery/          # Configuration principale
├── users/                  # Gestion des utilisateurs ✅
├── restaurants/            # Restaurants et menus ✅
├── orders/                # Système de commandes ✅
├── delivery/              # Gestion des livraisons ⏳
├── payments/              # Intégrations de paiement ⏳
├── notifications_app/      # Système de notifications ✅
├── analytics/             # Analyses et statistiques ⏳
├── static/               # Fichiers statiques
├── templates/            # Templates HTML
├── media/               # Fichiers uploadés
└── logs/                # Fichiers de logs
```

## 🌐 Accès aux Services

Une fois le serveur lancé :

- **Interface d'administration** : http://localhost:8000/admin/
- **Documentation API** : http://localhost:8000/api/docs/
- **API Schema** : http://localhost:8000/api/schema/

## 🔐 Authentification

### Créer un Superutilisateur
```bash
python manage.py createsuperuser
```

### Tester l'API
```bash
# Test d'inscription
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "user_type": "client",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Test de connexion
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin"
  }'
```

## 🐳 Docker (Optionnel)

Si vous préférez utiliser Docker :

```bash
# Installer Docker Desktop pour Windows
# Puis lancer avec docker-compose

docker-compose up -d
```

## 🧪 Tests

### Test Automatique
```bash
python test_api.py
```

### Test Manuel
1. Ouvrir http://localhost:8000/admin/
2. Se connecter avec le superutilisateur
3. Vérifier que tous les modèles sont visibles

## 📊 Vérification

### ✅ Ce qui fonctionne
- ✅ Configuration Django
- ✅ Modèles et migrations
- ✅ Interface d'administration
- ✅ Authentification JWT
- ✅ API endpoints de base
- ✅ Système de notifications personnalisé
- ✅ WebSockets configurés

### ⏳ À venir (Phases suivantes)
- ⏳ CRUD restaurants
- ⏳ Système de commandes
- ⏳ Intégrations de paiement
- ⏳ Livraisons temps réel

## 🆘 Support

Si vous rencontrez d'autres problèmes :

1. **Vérifiez les logs** : `python manage.py runserver --verbosity=2`
2. **Testez la configuration** : `python manage.py check`
3. **Vérifiez les migrations** : `python manage.py showmigrations`

## 🎉 Félicitations !

Votre plateforme de livraison de repas est maintenant fonctionnelle sur Windows ! 

**Phase 1 terminée avec succès** ✅