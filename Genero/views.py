from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Genero
from .serializer import GeneroSerializer

from Usuario.models import Usuario
from Usuario.serializer import UsernameSerializer

from Livro.models import Livro
from Livro.serializer import LivroSerializer

from Autor.models import Autor
from Autor.serializer import ListaAutoresSerializer

# Create your views here.

class StaffGeneroView(APIView):
    #Autorizações: Se está autenticado e se é parte da Staff
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        nome_genero = request.data.get('nome_genero')
        #Testa se o JSON veio sem nome_genero
        if nome_genero is None:
            return Response ({'status': 400, 'msg': 'Campo nome_genero é obrigatório'}, status = 400)
        genero = Genero.objects.create(nome_genero=nome_genero)
        genero.save()
        return Response ({'status': 201, 'msg': 'Cadastrado com SUCESSO'}, status = 201)
    
    def patch(self, request, genero_id):

        genero = Genero.objects.filter(id=genero_id)
        #Testa se esse id corresponde a algum genero
        if not genero.exists():
            return Response({'status': 404, 'msg': 'Genero não encontrado'}, status = 404)
        genero = genero.first()
        nome_genero = request.data.get('nome_genero')
        if nome_genero is None:
            return Response ({'status': 400, 'msg': 'Campo nome_genero é obrigatório'}, status = 400)
        genero.nome_genero = nome_genero
        genero.save()
        return Response({'status': 200, 'msg': 'Alterado com SUCESSO'}, status = 200)
    
    def delete(self, request, genero_id):
        genero = Genero.objects.filter(id=genero_id)
        if not genero.exists():
            return Response({'status': 404, 'msg': 'Genero não encontrado'}, status = 404)
        genero = genero.first()
        genero.delete()
        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)

class ListGeneroView(APIView):
    
    def get(self, request):  
        genero = Genero.objects.all()
        serial = GeneroSerializer(genero, many=True) 
        if len(serial.data) > 0:  
            return Response({'status': 200, 'Generos': serial.data},status=200)

        return Response({'status': 204, 'msg': 'No Content'}, status=204)
    
class ListUsuarioPorGeneroView(APIView):

    def get(self, request, genero_id):
        genero = Genero.objects.filter(id=genero_id)
        #Testa se esse id corresponde a algum genero
        if not genero.exists():
            return Response({'status': 404, 'msg': 'Genero não encontrado'}, status = 404)
        genero = genero.first()

        usuarios = Usuario.objects.filter(generos_favoritos = genero)
        serial = UsernameSerializer(usuarios, many = True)

        if len(serial.data) > 0:  
            return Response({'status': 200, 'Usuarios': serial.data},status=200)

        return Response({'status': 204, 'msg': 'No Content'}, status=204)

class ListLivrosPorGeneroView(APIView):

    def get(self, request, genero_id):
        genero = Genero.objects.filter(id=genero_id)
        #Testa se esse id corresponde a algum genero
        if not genero.exists():
            return Response({'status': 404, 'msg': 'Genero não encontrado'}, status = 404)
        genero = genero.first()

        usuarios = Livro.objects.filter(generos_livro = genero)
        serial = LivroSerializer(usuarios, many = True)

        if len(serial.data) > 0:  
            return Response({'status': 200, 'Livros': serial.data},status=200)

        return Response({'status': 204, 'msg': 'No Content'}, status=204)
    
class ListAutoresPorGeneroView(APIView):

    def get(self, request, genero_id):
        genero = Genero.objects.filter(id=genero_id)
        #Testa se esse id corresponde a algum genero
        if not genero.exists():
            return Response({'status': 404, 'msg': 'Genero não encontrado'}, status = 404)
        genero = genero.first()

        usuarios = Autor.objects.filter(generos_autor = genero)
        serial = ListaAutoresSerializer(usuarios, many = True)

        if len(serial.data) > 0:  
            return Response({'status': 200, 'Livros': serial.data},status=200)

        return Response({'status': 204, 'msg': 'No Content'}, status=204)
    
