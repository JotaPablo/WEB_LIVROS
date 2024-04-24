from django.db import models
from Genero.models import Genero

class Autor(models.Model):

    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    born_in = models.DateField()
    died_in = models.DateField(null = True, blank = True)
    generos_autor = models.ManyToManyField(Genero, blank = True)
    
    class Meta:
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nome
    
