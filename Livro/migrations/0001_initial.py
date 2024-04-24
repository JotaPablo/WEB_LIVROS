# Generated by Django 4.2.11 on 2024-04-22 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Autor', '0003_rename_generos_autor_generos_autor'),
        ('Genero', '0002_delete_genero_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('descricao', models.TextField(blank=True)),
                ('data_publicacao', models.DateField(blank=True)),
                ('n_paginas', models.IntegerField(blank=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Autor.autor')),
                ('generos_livro', models.ManyToManyField(to='Genero.genero')),
            ],
        ),
    ]