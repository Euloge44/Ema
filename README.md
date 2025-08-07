# 🍽️ Plateforme de Livraison de Repas

Une plateforme complète de livraison de repas développée avec Django, comprenant une interface web responsive et des APIs REST pour mobile.

## 🚀 Fonctionnalités

### 👥 Multi-Rôles Utilisateurs
- **Clients** : Recherche, commande, suivi en temps réel
- **Restaurants** : Gestion de menus, commandes, analytics
- **Livreurs** : Application mobile, optimisation de trajets
- **Administrateurs** : Panel de gestion complet

### 🔍 Système de Recherche Intelligent
- Filtres multiples (cuisine, prix, distance, note)
- Recherche par géolocalisation
- Suggestions basées sur l'historique

### 💳 Paiements Multi-Passerelles
- Stripe (cartes internationales)
- PayPal (portefeuilles électroniques)
- TMoney et Flooz (Togo)

### 📱 Temps Réel
- WebSockets pour mises à jour instantanées
- Géolocalisation des livreurs
- Notifications push

## 🛠️ Technologies

### Backend
- **Django 4.2+** avec Django REST Framework
- **PostgreSQL** avec PostGIS pour la géolocalisation
- **Redis** pour le cache et les sessions
- **Celery** pour les tâches asynchrones
- **JWT** pour l'authentification

### Frontend
- **HTML5, CSS3, JavaScript ES6+**
- **Bootstrap 5** pour le design responsive
- **Leaflet.js** pour les cartes

### Infrastructure
- **Docker** pour le déploiement
- **Nginx** comme reverse proxy
- **AWS S3** pour le stockage de fichiers

## 📋 Prérequis

- Python 3.11+
- PostgreSQL 15+ avec PostGIS
- Redis 7+
- Docker et Docker Compose (optionnel)

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd food-delivery-platform
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

### 5. Base de données
```bash
# Créer la base de données PostgreSQL avec PostGIS
createdb food_delivery

# Migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 7. Collecter les fichiers statiques
```bash
python manage.py collectstatic
```

### 8. Lancer le serveur
```bash
python manage.py runserver
```

## 🐳 Déploiement avec Docker

### 1. Lancer avec Docker Compose
```bash
docker-compose up -d
```

### 2. Migrations dans le conteneur
```bash
docker-compose exec web python manage.py migrate
```

### 3. Créer un superutilisateur
```bash
docker-compose exec web python manage.py createsuperuser
```

## 📚 API Documentation

L'API est documentée avec Swagger/OpenAPI :
- **URL** : `http://localhost:8000/api/docs/`
- **Schema** : `http://localhost:8000/api/schema/`

### Endpoints Principaux

#### Authentification
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/logout/` - Déconnexion
- `POST /api/auth/token/refresh/` - Rafraîchir le token

#### Utilisateurs
- `GET /api/auth/profile/` - Profil utilisateur
- `PUT /api/auth/profile/update/` - Mettre à jour le profil
- `POST /api/auth/location/update/` - Mettre à jour la localisation

#### Restaurants
- `GET /api/restaurants/` - Liste des restaurants
- `GET /api/restaurants/{id}/` - Détails d'un restaurant
- `GET /api/restaurants/{id}/menu/` - Menu d'un restaurant

#### Commandes
- `GET /api/orders/` - Liste des commandes
- `POST /api/orders/` - Créer une commande
- `GET /api/orders/{id}/` - Détails d'une commande

## 🏗️ Architecture

### Structure du Projet
```
food-delivery-platform/
├── food_delivery/          # Configuration principale
├── users/                  # Gestion des utilisateurs
├── restaurants/            # Restaurants et menus
├── orders/                # Système de commandes
├── delivery/              # Gestion des livraisons
├── payments/              # Intégrations de paiement
├── notifications/         # Système de notifications
├── analytics/             # Analyses et statistiques
├── static/               # Fichiers statiques
├── templates/            # Templates HTML
├── media/               # Fichiers uploadés
└── logs/                # Fichiers de logs
```

### Modèles de Données

#### Utilisateurs
- `User` - Modèle utilisateur principal
- `UserProfile` - Profil étendu
- `ClientProfile` - Profil spécifique client
- `RestaurantProfile` - Profil restaurant
- `DeliveryProfile` - Profil livreur
- `AdminProfile` - Profil administrateur

#### Restaurants
- `CuisineType` - Types de cuisine
- `Restaurant` - Informations restaurant
- `Category` - Catégories de plats
- `MenuItem` - Plats du menu
- `MenuItemOption` - Options personnalisables
- `Review` - Avis clients
- `Promotion` - Promotions et offres

## 🔧 Configuration

### Variables d'Environnement

Copiez `.env.example` vers `.env` et configurez :

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DB_NAME=food_delivery
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Paiements
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
```

## 🧪 Tests

### Lancer les tests
```bash
python manage.py test
```

### Tests avec couverture
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 Monitoring

### Logs
Les logs sont configurés dans `settings.py` :
- Fichier : `logs/django.log`
- Niveau : INFO

### Health Checks
- API : `GET /api/health/`
- Base de données : Vérification automatique
- Redis : Vérification automatique

## 🔒 Sécurité

### Mesures Implémentées
- **CSRF Protection** : Activée par défaut
- **XSS Protection** : Headers de sécurité
- **Rate Limiting** : Limitation des requêtes API
- **JWT Authentication** : Tokens sécurisés
- **Password Validation** : Règles de complexité
- **Django Axes** : Protection contre les attaques par force brute

## 🚀 Déploiement en Production

### 1. Configuration Production
```bash
# Modifier .env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
```

### 2. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 3. Migrations
```bash
python manage.py migrate
```

### 4. Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 food_delivery.wsgi:application
```

### 5. Nginx Configuration
Voir `nginx.conf` pour la configuration complète.

## 🤝 Contribution

### 1. Fork le projet
### 2. Créer une branche feature
```bash
git checkout -b feature/amazing-feature
```
### 3. Commit les changements
```bash
git commit -m 'Add amazing feature'
```
### 4. Push vers la branche
```bash
git push origin feature/amazing-feature
```
### 5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou support :
- **Email** : support@fooddelivery.com
- **Documentation** : [docs.fooddelivery.com](https://docs.fooddelivery.com)
- **Issues** : [GitHub Issues](https://github.com/your-repo/issues)

## 🗺️ Roadmap

### Phase 1 ✅ - Structure et Authentification
- [x] Configuration Django
- [x] Système d'utilisateurs multi-rôles
- [x] Authentification JWT
- [x] Modèles de base

### Phase 2 🔄 - Restaurants et Menus
- [x] Modèles restaurants et menus
- [ ] CRUD restaurants
- [ ] Gestion des menus
- [ ] Système de recherche

### Phase 3 📋 - Commandes et Paiements
- [ ] Modèles de commandes
- [ ] Système de paiement
- [ ] Intégration Stripe/PayPal

### Phase 4 🚚 - Livraisons
- [ ] Modèles de livraison
- [ ] Suivi temps réel
- [ ] Optimisation de trajets

### Phase 5 📊 - Analytics
- [ ] Dashboard analytics
- [ ] Rapports avancés
- [ ] Métriques business

---

**Développé avec ❤️ pour la communauté de livraison de repas**