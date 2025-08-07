# Dockerfile pour la plateforme de livraison de repas
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        gdal-bin \
        libgdal-dev \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . /app/

# Créer les répertoires nécessaires
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "food_delivery.wsgi:application"]