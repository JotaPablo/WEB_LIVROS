# Generated by Django 4.2.11 on 2024-04-22 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Autor', '0003_rename_generos_autor_generos_autor'),
        ('Usuario', '0003_usuario_generos_favoritos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='autor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Autor.autor'),
        ),
    ]
