from rest_framework import serializers
from .models import Livro
from Genero.models import Genero
from Genero.serializer import GeneroSerializer
from Autor.serializer import ListaAutoresSerializer
from Autor.models import Autor
from Avaliacao.models import Avaliacao
from django.db.models import Avg
from Status_Livro.models import Status_Livro

class LivroSerializer(serializers.ModelSerializer):
    autor = ListaAutoresSerializer()
    class Meta:
        model = Livro
        fields = ['id', 'titulo','autor']


class LivroSerializerDetaield(serializers.ModelSerializer):
    generos_livro = GeneroSerializer(many=True)
    autor = ListaAutoresSerializer()
    nota = serializers.SerializerMethodField()
    qntd_avaliacoes = serializers.SerializerMethodField()
    lido = serializers.SerializerMethodField()
    lendo = serializers.SerializerMethodField()
    quer_ler = serializers.SerializerMethodField()
    
    class Meta:
        model = Livro
        fields = ['id', 'titulo','autor', 'descricao', 'data_publicacao', 'n_paginas', 'qntd_avaliacoes','nota','generos_livro'
                  , 'lido', 'lendo', 'quer_ler']


    def get_nota(self, obj):
        nota = Avaliacao.objects.filter(livro_avaliado = obj).aggregate(Avg('nota'))
        return nota['nota__avg']

    def get_qntd_avaliacoes(self, obj):
        avaliacoes = Avaliacao.objects.filter(livro_avaliado  = obj)
        return len(avaliacoes)
    
    def get_lido(self, obj):
        livro = Status_Livro.objects.filter(livro = obj, status = 1)
        return len(livro)


    def get_lendo(self, obj):
        livro = Status_Livro.objects.filter(livro = obj, status = 2)
        return len(livro)

    def get_quer_ler(self, obj):
        livro = Status_Livro.objects.filter(livro = obj, status = 3)
        return len(livro)



