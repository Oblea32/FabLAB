from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Curso

# Usamos UserAdmin para manejar el modelo CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_type', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'is_active', 'is_staff')}
        ),
    )

    def save_model(self, request, obj, form, change):
        # Asegúrate de que la contraseña se encripte al guardar un nuevo usuario
        if not change:  # Solo cuando el usuario es nuevo
            obj.set_password(obj.password)  # Encripta la contraseña antes de guardarla
        super().save_model(request, obj, form, change)



@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'docente')  # Muestra estos campos en la lista
    search_fields = ('nombre', 'descripcion')  # Permite buscar por estos campos
    list_filter = ('docente',)  # Permite filtrar por docente
    filter_horizontal = ('estudiantes',)  # Muestra los estudiantes con un filtro horizontal



