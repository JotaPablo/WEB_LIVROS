from rest_framework import serializers
from .models import Avaliacao, Comentario
from Livro.models import Livro
from Usuario.models import Usuario

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['titulo','id']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','id']

class AvaliacaoSerializer(serializers.ModelSerializer):
  
    livro_avaliado = LivroSerializer()
    usuario_avaliando = UsuarioSerializer()

    class Meta:
        model = Avaliacao
        fields = ['id','livro_avaliado', 'usuario_avaliando', 'nota', 'descricao', 'data_avaliacao']

class ComentarioSerializer(serializers.ModelSerializer):

    avaliacao_comentada  = serializers.SerializerMethodField()
    usuario_comentando = UsuarioSerializer()

    class Meta:
        
        model = Comentario
        fields = ['id','avaliacao_comentada', 'usuario_comentando', 'descricao', 'data_comentario']

    def get_avaliacao_comentada(self, obj):
            return obj.avaliacao_comentada.id