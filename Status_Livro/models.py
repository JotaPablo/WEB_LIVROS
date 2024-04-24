from django.db import models
from Livro.models import Livro
from Usuario.models import Usuario

# Create your models here.
class Status_Livro(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #Status:
    # 1 - Lido
    # 2 - Lendo
    # 3 - Quer_Ler
    status = models.IntegerField()