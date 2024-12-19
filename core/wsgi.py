"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Asegúrate de que la carpeta raíz 'fablab' esté en el sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configura el entorno de Django para usar el archivo settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

app = application
