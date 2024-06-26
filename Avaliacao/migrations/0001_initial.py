# Generated by Django 4.2.11 on 2024-04-23 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Livro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField()),
                ('descricao', models.TextField()),
                ('data_avaliacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('livro_avaliado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Livro.livro')),
                ('usuario_avaliando', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('data_comentario', models.DateTimeField(default=django.utils.timezone.now)),
                ('avaliacao_comentada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Avaliacao.avaliacao')),
                ('usuario_comentando', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
