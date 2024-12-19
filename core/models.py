from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User  # Importar modelo de usuario
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('admin', 'Administrador'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='estudiante')

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.assign_group()

    def assign_group(self):
        if self.user_type == 'estudiante':
            grupo, _ = Group.objects.get_or_create(name='Estudiantes')
        elif self.user_type == 'docente':
            grupo, _ = Group.objects.get_or_create(name='Docentes')
        elif self.user_type == 'admin':
            grupo, _ = Group.objects.get_or_create(name='Administradores')
            self.is_staff = True
            self.is_superuser = True
            self.save()
        
        self.groups.add(grupo)



class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    docente = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'docente'})
    estudiantes = models.ManyToManyField(CustomUser, related_name='cursos_inscritos', limit_choices_to={'user_type': 'estudiante'}, blank=True)

    def __str__(self):
        return self.nombre
    

class MaterialCurso(models.Model):
    curso = models.ForeignKey(Curso, related_name='materiales', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='materiales_cursos/', null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=[('pdf', 'PDF'), ('word', 'Word'), ('ppt', 'PPT'), ('excel', 'Excel'), ('imagen', 'Imagen'), ('otro', 'Otro')])
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    

@receiver(post_save, sender=CustomUser)
def ensure_user_in_group(sender, instance, created, **kwargs):
    if instance.user_type == 'docente':
        grupo_docentes, _ = Group.objects.get_or_create(name='Docentes')
        instance.groups.add(grupo_docentes)
