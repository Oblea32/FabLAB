# Generated by Django 5.1.2 on 2024-10-20 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0003_alter_noticias_options_alter_noticias_imagen'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='noticias',
            new_name='Noticia',
        ),
    ]