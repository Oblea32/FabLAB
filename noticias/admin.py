from django.contrib import admin
from .models import Noticia

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'image_tag', 'fecha_creacion', 'fecha_actualizacion')
    readonly_fields = ('image_tag',)  

admin.site.register(Noticia, NoticiaAdmin)
