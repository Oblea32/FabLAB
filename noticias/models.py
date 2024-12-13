from django.db import models
from django.utils.html import mark_safe

class Noticia(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField()
    imagen=models.ImageField(upload_to='noticias/')
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    fecha_actualizacion=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Noticia"
        verbose_name_plural="Noticias"

    def __str__ (self):
        return "Titulo: "+self.nombre


    def image_tag(self):
        if self.imagen:
            return mark_safe(f'<img src="{self.imagen.url}" width="150" height="150" />')
        return "(No image)"

    image_tag.short_description = 'Imagen'



