# Generated by Django 4.2.11 on 2024-04-21 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Genero', '0002_delete_genero_usuario'),
        ('Autor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='autor',
            name='generos',
            field=models.ManyToManyField(blank=True, to='Genero.genero'),
        ),
        migrations.AlterField(
            model_name='autor',
            name='descricao',
            field=models.TextField(),
        ),
    ]
