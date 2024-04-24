from rest_framework import serializers
from .models import Autor
from Genero.serializer import GeneroSerializer

class ListaAutoresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Autor
        fields = ['id', 'nome']

class AutorSerializerDetaield(serializers.ModelSerializer):
   
    generos_autor = GeneroSerializer(many=True)
   
    class Meta:
        model = Autor
        fields = ['nome', 'descricao', 'born_in', 'died_in','generos_autor']
