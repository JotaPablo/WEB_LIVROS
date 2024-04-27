from rest_framework import serializers
from .models import Status_Livro
from Livro.serializer import LivroSerializer
from Avaliacao.models import Avaliacao
from Avaliacao.serializer import AvaliacaoSerializer
from Usuario.serializer import UsernameSerializer

class AvaliacaoLidoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Avaliacao
        fields = ['id', 'nota', 'descricao', 'data_avaliacao']


class LidoSerializer(serializers.ModelSerializer):

    livro = LivroSerializer()
    avaliacao = serializers.SerializerMethodField()

    class Meta:
        model = Status_Livro
        fields = ['livro','avaliacao']

    def get_avaliacao(self, obj):
        usuario = obj.usuario
        livro = obj.livro
        avaliacao = Avaliacao.objects.filter(usuario_avaliando=usuario, livro_avaliado = livro)

        if not avaliacao.exists():
            return None
        else:
            avaliacao = avaliacao.first()
            return AvaliacaoLidoSerializer(avaliacao).data


class ListaLivroSerializer(serializers.ModelSerializer):

    livro = LivroSerializer()

    class Meta:
        model = Status_Livro
        fields = ['livro']

class ListaUsuarioSerializer(serializers.ModelSerializer):

    usuario = UsernameSerializer()

    class Meta:
        model = Status_Livro
        fields = ['usuario']