from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User  # Importar modelo de usuario
from django.utils.timezone import now


class Saga(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='sagas/', null=True, blank=True, verbose_name="Imagen")
    publicado = models.DateTimeField(default=now, verbose_name="Publicado")  # Campo para marcar publicación
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")  # Relación con el autor
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")  # Fecha de creación
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")  # Fecha de actualización

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Saga"
        verbose_name_plural = "Sagas"
        ordering = ['creado']  # Ordenar por fecha de creación descendente

    def image_tag(self):
        if self.imagen:
            return mark_safe(f'<img src="{self.imagen.url}" width="150" height="150" style="height: 250px; object-fit: contain;" />')
        return "(No image)"
    image_tag.short_description = 'Imagen'


class Personajes(models.Model):
    nombre = models.CharField(max_length=100)
    saga = models.ManyToManyField(Saga, related_name='personajes')
    imagen = models.ImageField(upload_to='personajes/', null=True, blank=True, verbose_name="Imagen")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Personaje"
        verbose_name_plural = "Personajes"

    def image_tag(self):
        if self.imagen:
            return mark_safe(f'<img src="{self.imagen.url}" width="150" height="150" style="height: 250px; object-fit: contain;" />')  # Agranda la imagen
        return "(No image)"
    image_tag.short_description = 'Imagen'


class Enemigos(models.Model):
    nombre = models.CharField(max_length=100)
    saga = models.ManyToManyField(Saga, related_name='enemigos')
    imagen = models.ImageField(upload_to='enemigos/', null=True, blank=True, verbose_name="Imagen")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Enemigo"
        verbose_name_plural = "Enemigos"

    def image_tag(self):
        if self.imagen:
            return mark_safe(f'<img src="{self.imagen.url}" width="150" height="150" style="height: 250px; object-fit: contain;" />')  # Agranda la imagen
        return "(No image)"
    image_tag.short_description = 'Imagen'

