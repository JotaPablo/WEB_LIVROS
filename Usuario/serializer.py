from rest_framework import serializers
from .models import Usuario
from Pais.serializer import PaisSerializer
from Genero.serializer import GeneroSerializer
from Autor.serializer import ListaAutoresSerializer
from Status_Livro.models import Status_Livro

#Um serializer básico pra listar todos os usuários ou os privados(Usado em UserView,)
class UsernameSerializer(serializers.ModelSerializer):

    pais = PaisSerializer()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'data_joined', 'pais', 'is_private']


#Um pra pesquisar um usuário especifico e se não for privado
#mostrar descrição, generos favoritos, quando entrou, quantos livros já leu, está lendo ou quer ler e quantas avaliações fez
class UsuarioSerializer(serializers.ModelSerializer):

    autor = ListaAutoresSerializer()
    pais = PaisSerializer()
    generos_favoritos = GeneroSerializer(many=True)
    lidos = serializers.SerializerMethodField()
    lendo = serializers.SerializerMethodField()
    quer_ler = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'data_joined', 'descricao','autor',  'pais', 'generos_favoritos', 'is_private', 'lidos', 'lendo', 'quer_ler']
    
    #A quantidade de livros que leu, está lendo ou quer_ler
    #Mais informalções sobre quais são esses livros nas views de Status_Livro
    def get_lidos(self, obj):
        usuario = obj
        status = Status_Livro.objects.filter(usuario = usuario, status = 1)
        return len(status)
    
    def get_lendo(self, obj):
        usuario = obj
        status = Status_Livro.objects.filter(usuario = usuario, status = 2)
        return len(status)
    
    def get_quer_ler(self, obj):
        usuario = obj
        status = Status_Livro.objects.filter(usuario = usuario, status = 3)
        return len(status)


#Um pra mostrar tudo isso do de cima mas as informações pessoais dos usuários como telefone, email e tudo mais
class EuSerializer(serializers.ModelSerializer):

    autor = ListaAutoresSerializer()
    pais = PaisSerializer()
    generos_favoritos = GeneroSerializer(many=True)
    lidos = serializers.SerializerMethodField()
    lendo = serializers.SerializerMethodField()
    quer_ler = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nome', 'email', 'telefone', 'data_joined', 'autor', 
                 'descricao','pais', 'generos_favoritos', 'is_private', 'lidos', 'lendo', 'quer_ler']
        
    #A quantidade de livros que leu, está lendo ou quer_ler
    #Mais informalções sobre quais são esses livros nas views de Status_Livro
    def get_lidos(self, obj):
        usuario = obj
        status = Status_Livro.objects.filter(usuario = usuario, status = 1)
        return len(status)
    
    def get_lendo(self, obj):
        usuario = obj
        status = Status_Livro.objects.filter(usuario = usuario, status = 2)
        return len(status)
    
    def get_quer_ler(self, obj):
        usuario = obj
        status = Status_Livro.objects.filter(usuario = usuario, status = 3)
        return len(status)





