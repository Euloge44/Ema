"""
Configuration Celery pour les tâches asynchrones.
"""
import os
from celery import Celery

# Définir le module de paramètres par défaut pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

app = Celery('food_delivery')

# Utiliser une chaîne ici signifie que le worker n'a pas à sérialiser
# l'objet de configuration vers les processus enfants.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches depuis tous les modules de tâches enregistrés
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Tâche de débogage pour tester Celery."""
    print(f'Request: {self.request!r}')