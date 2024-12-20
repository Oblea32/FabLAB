from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),

     # Rutas de la aplicación 'core' directamente aquí
    path('', views.index, name='index'),  # Ruta para la página de inicio
    path('galeria/', views.galeria, name='galeria'),  # Ruta para la galería
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),  # Ruta para quiénes somos
    path('contacto/', views.contacto, name='contacto'),  # Ruta para contacto
    path('servicios/', views.servicios, name='servicios'),  # Ruta para servicios
    path('register/', views.register, name='register'),
    path('crear-docente/', views.crear_docente, name='crear_docente'),
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('curso/<int:curso_id>/gestionar/', views.gestionar_curso, name='gestionar_curso'),
    path('ambiente/', views.ambiente, name='ambiente'),
    path('ambiente/estudiante/', views.ambiente_estudiante, name='ambiente_estudiante'),
    path('curso/detalles/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('curso/<int:curso_id>/inscribir/', views.inscribir_curso, name='inscribir_curso'),
    path('ambiente/docente/', views.ambiente_docente, name='ambiente_docente'),
    path('curso/<int:curso_id>/editar/', views.editar_curso, name='editar_curso'),
    path('curso/<int:curso_id>/lista-excel/', views.lista_alumnos_excel, name='lista_alumnos_excel'),
    path('curso/<int:curso_id>/lista-pdf/', views.lista_alumnos_pdf, name='lista_alumnos_pdf'),
    path('curso/<int:curso_id>/subir_material/', views.subir_material, name='subir_material'),
    path('material/eliminar/<int:material_id>/', views.eliminar_material, name='eliminar_material'),
# Rutas para el manejo de autenticación
    path('login/', views.login_view, name='login'),  # Usa tu vista personalizada
    path('logout/', views.logout_view, name='logout'),  # Usa tu vista de logout

]


# Añadir las URLs de archivos estáticos
urlpatterns += staticfiles_urlpatterns()

# Archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



   