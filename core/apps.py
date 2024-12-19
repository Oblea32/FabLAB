from django.conf import settings
from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
    if settings.DEBUG is False:  # Solo se aplica en producción
        path = '/opt/render/project/src/core'  # Ruta específica de Render
