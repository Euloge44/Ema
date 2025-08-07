#!/usr/bin/env python3
"""
Script pour lancer le serveur Django avec debug détaillé.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Lancer le serveur avec debug."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
    
    # Configuration pour debug
    os.environ['DJANGO_DEBUG'] = 'True'
    
    # Lancer le serveur avec verbosité maximale
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000', '--verbosity=3', '--traceback']
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()