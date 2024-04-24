from django.db import models
from Livro.models import Livro
from Usuario.models import Usuario
from django.utils import timezone

class Avaliacao(models.Model):
    livro_avaliado = models.ForeignKey(Livro, on_delete = models.CASCADE)
    usuario_avaliando = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    nota = models.IntegerField()
    descricao = models.TextField()
    data_avaliacao = models.DateTimeField(default=timezone.now)

class Comentario(models.Model):
    avaliacao_comentada = models.ForeignKey(Avaliacao,on_delete = models.CASCADE)
    usuario_comentando = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    descricao = models.TextField()
    data_comentario = models.DateTimeField(default=timezone.now)
    