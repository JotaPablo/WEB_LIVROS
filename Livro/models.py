from django.db import models
from Autor.models import Autor
from Genero.models import Genero


class Livro(models.Model):
    #capa
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank = True)
    data_publicacao = models.DateField(blank = True)
    n_paginas = models.IntegerField(blank = True)
    autor = models.ForeignKey(Autor, on_delete = models.CASCADE)
    generos_livro = models.ManyToManyField(Genero)

    def __str__(self):
        return self.titulo
    