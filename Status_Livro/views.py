from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Status_Livro
from Usuario.models import Usuario
from Livro.models import Livro

from .serializer import LidoSerializer, ListaLivroSerializer, ListaUsuarioSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class ListaStatusView(APIView):
    def get(self, request, status, usuario_id):
        usuario = Usuario.objects.filter(id = usuario_id)
        if not usuario.exists():
            return Response({'status': 404, 'msg': 'Usuario não encontrado'})
        
        usuario = usuario.first()
        if usuario.is_private:
            return Response({'status': 403, 'msg': 'Usuário é privado!'}, status = 403)
        
        if status < 1 or status > 3:
            return Response({'status': 400, 'msg': 'Status precisa ser entre 1 e 3'}, status = 400)


        status_livro = Status_Livro.objects.filter(usuario=usuario, status=status)
        if status == 1: 
            serial = LidoSerializer(status_livro, many=True)
        else:
            serial = ListaLivroSerializer(status_livro, many = True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No content'}, status = 204)

class UsuarioStatusView(APIView):

    #Autorizações: Se é está autenticado
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get(self, request, status):
        usuario = request.user

        if status < 1 or status > 3:
            return Response({'status': 400, 'msg': 'Status precisa ser entre 1 e 3'}, status = 400)

        status_livro = Status_Livro.objects.filter(usuario=usuario, status=status)
        if status == 1: 
            serial = LidoSerializer(status_livro, many=True)
        else:
            serial = ListaLivroSerializer(status_livro, many = True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No content'}, status = 204)
        
    def post(self, request, livro_id, status):

        livro = Livro.objects.filter(id = livro_id)

        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)
        
        livro = livro.first()

        usuario = request.user

        if status < 1 or status > 3:
            return Response({'status': 400, 'msg': 'Status precisa ser entre 1 e 3'}, status = 400)
        
        status_livro = Status_Livro.objects.filter(usuario=usuario, livro=livro)

        if status_livro.exists():
            status_livro = status_livro.first()
            status_livro.status_livro = status
            status_livro.save()

        else:
            status_livro = Status_Livro.objects.create(livro = livro, usuario = usuario, status = status)
            status_livro.save()
        
        return Response({'status': 201, 'msg': 'registered successfully'})

class UsuarioDeletaStatusView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def delete(self, request, livro_id):

        livro = Livro.objects.filter(id = livro_id)

        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)
        
        livro = livro.first()
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, livro=livro)
        
        if not status.exists():
            return Response({'status': 404, 'msg': 'Usuário não tem esse livro na sua prateleira'}, status = 404)
        
        status = status.first()
        status.delete()
        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)
        
class ListaStatusLivroView(APIView):
    def get(self, request, livro_id, status):

        #Checa se esse livro existe
        livro = Livro.objects.filter(id = livro_id)

        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)
        
        livro = livro.first()

        if status < 1 or status > 3:
            return Response({'status': 400, 'msg': 'Status precisa ser entre 1 e 3'}, status = 400)

        usuario = Status_Livro.objects.filter(livro = livro, usuario__is_private = False, status = status)

        serial = ListaUsuarioSerializer(usuario, many = True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Usuários': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No Content'}, status=204)

