from rest_framework.views import APIView


from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Pais
from .serializer import PaisSerializer

from Usuario.models import Usuario
from Usuario.serializer import UsernameSerializer

# Create your views here.

class StaffPaisView(APIView):
    #Autorizações: Se está autenticado e se é parte da Staff
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        #Testa se nome_pais é None, pois é um campo obrigatório
        nome_pais = request.data.get('nome_pais')
        if nome_pais is None:
            return Response ({'status': 400, 'msg': 'Campo nome_país é obrigatório'}, status = 400)
        pais = Pais.objects.create(nome_pais=nome_pais)
        pais.save()
        return Response ({'status': 201, 'msg': 'Cadastrado com SUCESSO'}, status = 201)
    
    def patch(self, request, pais_id):
        #Testa se o id corresponde á algum pais
        pais = Pais.objects.filter(id=pais_id)
        if not pais.exists():
            return Response({'status': 404, 'msg': 'Pais não encontrado'}, status = 404)
        pais = pais.first()

        #Testa se nome_pais é None, pois é um campo obrigatório
        nome_pais = request.data.get('nome_pais')
        if nome_pais is None:
            return Response ({'status': 400, 'msg': 'Campo nome_pais é obrigatório'}, status = 400)
        pais.nome_pais = nome_pais

        pais.save()
        return Response({'status': 200, 'msg': 'Alterado com SUCESSO'}, status = 200)
        
    def delete(self, request, pais_id):
        #Testa se o id corresponde á algum pais
        pais = Pais.objects.filter(id=pais_id)
        if not pais.exists():
            return Response({'status': 404, 'msg': 'Pais não encontrado'}, status = 404)
        pais = pais.first()
        pais.delete()

        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)

        
class ListPaisView(APIView):
    
    def get(self, request):
        pais = Pais.objects.all()
        serial = PaisSerializer(pais, many = True)
        if len(serial.data) > 0:
            return Response({'status': 302, 'Pais': serial.data}, status= 302)
        
        return Response({'status': 204, 'msg': 'No Content'}, status = 204)
    
    #def lista usuarios de um pais especifico
    
class UsuarioPaisView(APIView):
    
    def get(self, request, pais_id):
        #Testa se o id corresponde á algum pais
        pais = Pais.objects.filter(id=pais_id)
        if not pais.exists():
            return Response({'status': 404, 'msg': 'País não encontrado'}, status=404)
        #Busca em Usuário os que tem esse mesmo pais_id
        usuario = Usuario.objects.filter(pais = pais_id)
        serial = UsernameSerializer(usuario, many = True)
        if len(serial.data) > 0:
            return Response({
                'status': 302, 'Usuarios do Pais': serial.data
            })
        return Response({'status': 204, 'msg': 'No Content'})
    


        

    
