from rest_framework import serializers
from .models import Livro
from Genero.models import Genero
from Genero.serializer import GeneroSerializer
from Autor.serializer import ListaAutoresSerializer
from Autor.models import Autor

class LivroSerializer(serializers.ModelSerializer):
    autor = ListaAutoresSerializer()
    class Meta:
        model = Livro
        fields = ['id', 'titulo','autor']


class LivroSerializerDetaield(serializers.ModelSerializer):
    generos_livro = GeneroSerializer(many=True)
    autor = ListaAutoresSerializer()
    
    class Meta:
        model = Livro
        fields = ['id', 'titulo','autor', 'descricao', 'data_publicacao', 'n_paginas', 'generos_livro']

    