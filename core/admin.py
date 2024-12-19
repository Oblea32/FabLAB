from django.contrib import admin
from .models import CustomUser, Curso

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_type', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')



@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'docente')  # Muestra estos campos en la lista
    search_fields = ('nombre', 'descripcion')  # Permite buscar por estos campos
    list_filter = ('docente',)  # Permite filtrar por docente
    filter_horizontal = ('estudiantes',)  # Muestra los estudiantes con un filtro horizontal



