from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Status_Livro
from Usuario.models import Usuario
from Livro.models import Livro

from .serializer import LidoSerializer, ListaLivroSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class ListaLidosUsuarioView(APIView):
    def get(self, request, usuario_id):
        usuario = Usuario.objects.filter(id = usuario_id)
        if not usuario.exists():
            return Response({'status': 404, 'msg': 'Usuario não encontrado'})
        
        usuario = usuario.first()
        if usuario.is_private:
            return Response({'status': 403, 'msg': 'Usuário é privado!'}, status = 403)


        status = Status_Livro.objects.filter(usuario=usuario, status = 1)
        serial = LidoSerializer(status, many = True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No content'}, status = 204)
        

class ListaLendoUsuarioView(APIView):
    def get(self, request, usuario_id):
        usuario = Usuario.objects.filter(id = usuario_id)
        if not usuario.exists():
            return Response({'status': 404, 'msg': 'Usuario não encontrado'})
        
        usuario = usuario.first()
        if usuario.is_private:
            return Response({'status': 403, 'msg': 'Usuário é privado!'}, status = 403)


        status = Status_Livro.objects.filter(usuario=usuario, status = 2)
        serial = ListaLivroSerializer(status, many = True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No content'}, status = 204)

class ListaQuerLerUsuarioView(APIView):
    def get(self, request, usuario_id):
        usuario = Usuario.objects.filter(id = usuario_id)
        if not usuario.exists():
            return Response({'status': 404, 'msg': 'Usuario não encontrado'})
        
        usuario = usuario.first()
        if usuario.is_private:
            return Response({'status': 403, 'msg': 'Usuário é privado!'}, status = 403)


        status = Status_Livro.objects.filter(usuario=usuario, status = 3)
        serial = ListaLivroSerializer(status, many = True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No content'}, status = 204)



class UsuarioLidoView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #get
    def get(self, request):
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, status=1)
        serial = LidoSerializer(status, many=True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No content'}, status = 204)

    #post
    def post(self, request, livro_id):

        livro = Livro.objects.filter(id = livro_id)

        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)
        
        livro = livro.first()
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, livro=livro)

        if status.exists():
            status = status.first
            status.status = 1
            status.save()

        else:
            status = Status_Livro.objects.create(livro = livro, usuario = usuario, status = 1)
            status.save()
        
        return Response({'status': 201, 'msg': 'registered successfully'})
        
class UsuarioLendoView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, status = 2)
        serial = ListaLivroSerializer(status, many=True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No Content'}, status=204)

    #post
    def post(self, request, livro_id):

        livro = Livro.objects.filter(id = livro_id)

        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)
        
        livro = livro.first()
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, livro=livro)

        if status.exists():
            status = status.first
            status.status = 2
            status.save()

        else:
            status = Status_Livro.objects.create(livro = livro, usuario = usuario, status = 2)
            status.save()
        
        return Response({'status': 201, 'msg': 'registered successfully'})
        
class UsuarioQuerLerView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #get
    def get(self, request):
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, status = 3)
        serial = ListaLivroSerializer(status, many=True)

        if len(serial.data) > 0:
            return Response({
                'status': 302,
                'Livros': serial.data
            }, status = 302)
        else:
            return Response({'status': 204, 'msg': 'No Content'}, status=204)

    #post
    def post(self, request, livro_id):

        livro = Livro.objects.filter(id = livro_id)

        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)
        
        livro = livro.first()
        usuario = request.user

        status = Status_Livro.objects.filter(usuario=usuario, livro=livro)

        if status.exists():
            status = status.first
            status.status = 2
            status.save()

        else:
            status = Status_Livro.objects.create(livro = livro, usuario = usuario, status = 3)
            status.save()
        
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
        
