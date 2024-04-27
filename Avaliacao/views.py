
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Avaliacao, Comentario
from Livro.models import Livro
from Usuario.models import Usuario
from .serializer import (
    LivroSerializer,
    UsuarioSerializer,
    AvaliacaoSerializer,
    ComentarioSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

#Lista todas as avaliacoes de um livro
class AvaliacaoListAPIView(APIView):
    def get(self, request, livro_id):
        avaliacoes = Avaliacao.objects.filter(livro_avaliado_id=livro_id)
        
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)
    
#Lista todos os comentarios de uma avaliacao
class ComentariosListAPIView(APIView):
     def get(self, request, avaliacao_id):
        comentarios = Comentario.objects.filter(avaliacao_comentada_id=avaliacao_id)
        
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data)

#staff deleta avaliacao
class StaffDeletaAvalaiacao(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, avaliacao_id):
        try:
            avaliacao = Avaliacao.objects.get(id=avaliacao_id)
            avaliacao.delete()
            return Response({'status': 204, 'msg': 'deleted successfully'})
        except Avaliacao.DoesNotExist:
            return Response({'status': 404, 'msg': 'Avaliacao not found'})

#staff deleta comentario
class StaffDeletaComentario(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, comentario_id):
        try:
            comentario = Comentario.objects.get(id=comentario_id)
            comentario.delete()
            return Response({'status': 204, 'msg': 'deleted successfully'})
        except Comentario.DoesNotExist:
            return Response({'status': 404, 'msg': 'Comentario not found'})




     


class AvaliacaoCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
            
            livro_avaliado = request.data.get('livro_avaliado')
            livro_avaliado = Livro.objects.filter(id = livro_avaliado)
            if not livro_avaliado.exists():
                return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)

            livro_avaliado = livro_avaliado.first()
            usuario_avaliando = request.user

            #Testa se o usuário já avaliou esse livro, pois só pode haver uma avalição por usuário em cada livro
            avaliacao = Avaliacao.objects.filter(livro_avaliado=livro_avaliado, usuario_avaliando=usuario_avaliando)

            if avaliacao.exists():
                return Response({'status': 403, 'msg': 'Esse usuário já avaliou esse livro'}, status = 403)

            nota = request.data.get('nota')
            if nota is None:
                return Response({'status': 400, 'msg': 'Campo nota é obrigatório!'}, status = 400)
            if nota < 0 or nota > 5:
                 return Response({'status': 400, 'msg': 'Nota precisa ser menor que 5 e maior que 0'}, status = 400)
               
            descricao = request.data.get('descricao')
            
            avaliacao = Avaliacao.objects.create(livro_avaliado=livro_avaliado,usuario_avaliando=usuario_avaliando,nota=nota,descricao=descricao)  
            avaliacao.save()
            return Response({'status': 201, 'msg': 'registered successfully'})
    
    def delete(self, request, avaliacao_id):
        try:
            avaliacao = Avaliacao.objects.get(id=avaliacao_id)
            usuario = request.user
            if usuario != avaliacao.usuario_avaliando:
                return Response({'status': 401, 'msg': 'Avaliação não foi feito por esse usuário'}, status = 401)

            avaliacao.delete()
            return Response({'status': 204, 'msg': 'deleted successfully'})
        except Avaliacao.DoesNotExist:
            return Response({'status': 404, 'msg': 'Avaliacao not found'})


class ComentarioCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
            avaliacao_comentada = request.data.get('avaliacao_comentada')
            if avaliacao_comentada is None:
                return Response({'status': 400, 'msg': 'Campo avaliacao_comentada é obrigatório!'}, status = 400)
            avaliacao_comentada = Avaliacao.objects.filter(id = avaliacao_comentada)
            avaliacao_comentada = avaliacao_comentada.first()
            usuario_comentando = request.user
            descricao = request.data.get('descricao')
            if descricao is None:
                return Response({'status': 400, 'msg': 'Campo descricao é obrigatório!'}, status = 400)
            
            comentario = Comentario.objects.create(avaliacao_comentada=avaliacao_comentada,usuario_comentando=usuario_comentando,descricao=descricao)  
            comentario.save()
            return Response({'status': 201, 'msg': 'registered successfully'})
    
    def delete(self, request, comentario_id):
        try:
            comentario = Comentario.objects.get(id=comentario_id)
            usuario = request.user
            if usuario != comentario.usuario_comentando:
                return Response({'status': 401, 'msg': 'Comentário não foi feito por esse usuário'}, status = 401)
            comentario.delete()
            return Response({'status': 204, 'msg': 'deleted successfully'})
        except Comentario.DoesNotExist:
            return Response({'status': 404, 'msg': 'Comentario not found'})
