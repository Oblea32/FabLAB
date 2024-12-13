# Generated by Django 5.1.3 on 2024-11-18 02:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Saga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='sagas/', verbose_name='Imagen')),
                ('publicado', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publicado')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Saga',
                'verbose_name_plural': 'Sagas',
                'ordering': ['-creado'],
            },
        ),
        migrations.CreateModel(
            name='Personajes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='personajes/', verbose_name='Imagen')),
                ('saga', models.ManyToManyField(related_name='personajes', to='core.saga')),
            ],
            options={
                'verbose_name': 'Personaje',
                'verbose_name_plural': 'Personajes',
            },
        ),
        migrations.CreateModel(
            name='Enemigos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='enemigos/', verbose_name='Imagen')),
                ('saga', models.ManyToManyField(related_name='enemigos', to='core.saga')),
            ],
            options={
                'verbose_name': 'Enemigo',
                'verbose_name_plural': 'Enemigos',
            },
        ),
    ]