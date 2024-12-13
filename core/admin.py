from django.contrib import admin
from django.utils.html import mark_safe
from .models import Saga, Personajes, Enemigos

class SagaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'autor', 'image_tag', 'creado', 'actualizado', 'publicado')
    list_filter = ('publicado', 'autor', 'creado')
    search_fields = ('nombre', 'descripcion', 'autor__username')
    readonly_fields = ('creado', 'actualizado', 'image_tag')

    def image_tag(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="150" height="150" style="height: 250px; object-fit: contain;"/>')
        return "No hay imagen"
    image_tag.short_description = 'Imagen'


class PersonajesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'image_tag')  # Mostrar imagen en el admin
    filter_horizontal = ('saga',)

    def image_tag(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="150" height="150" style="height: 250px; object-fit: contain;"/>')
        return "No hay imagen"
    image_tag.short_description = 'Imagen'


class EnemigosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'image_tag')  # Mostrar imagen en el admin
    filter_horizontal = ('saga',)

    def image_tag(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="150" height="150" style="height: 250px; object-fit: contain;"/>')
        return "No hay imagen"
    image_tag.short_description = 'Imagen'


admin.site.register(Saga, SagaAdmin)
admin.site.register(Personajes, PersonajesAdmin)
admin.site.register(Enemigos, EnemigosAdmin)




