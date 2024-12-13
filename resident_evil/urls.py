from django.contrib import admin
from django.urls import path, include
from core import views as core_views  
from noticias import views as noticias_views  
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),

     # Rutas de la aplicación 'core' directamente aquí
    path('', core_views.index, name='index'),  # Ruta para la página de inicio
    path('galeria/', core_views.galeria, name='galeria'),  # Ruta para la galería
    path('quienes_somos/', core_views.quienes_somos, name='quienes_somos'),  # Ruta para quiénes somos
    path('contacto/', core_views.contacto, name='contacto'),  # Ruta para contacto
    path('noticias/', noticias_views.noticias, name='noticias'),  # Ruta para noticias
    path('servicios/', core_views.servicios, name='servicios'),  # Ruta para servicios
    path('register/', core_views.register, name='register'),  # Ruta para registro
    path('informacion/', core_views.informacion, name='informacion'),
    path('sagas/', core_views.lista_sagas, name='sagas'),

# Rutas para el manejo de autenticación
    path('accounts/', include('django.contrib.auth.urls')),  # Incluye las URLs de autenticación (login, logout, etc.)
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Ruta de logout

]

# Añadir las URLs de archivos estáticos
urlpatterns += staticfiles_urlpatterns()

# Archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



   