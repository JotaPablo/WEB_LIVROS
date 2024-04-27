from rest_framework.views import APIView
from .models import Usuario
from .serializer import UsernameSerializer, UsuarioSerializer, EuSerializer
from Pais.models import Pais
from Genero.models import Genero
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from Autor.models import Autor

# Create your views here.

#Se Cadastrar
class RegisterView(APIView):

    def post(self, request):
        #Testa se o campo username é None ou se o username já está sendo utilizado
        username = request.data.get('username')
        if username is None:
            return Response({'status': 400, 'msg': 'O campo Username é obrigatório!'}, status = 400)
        user_exists = Usuario.objects.filter(username=username).exists()
        if user_exists:
           return Response({'status': 409, 'msg': 'Username já existente!'})
        
        #Testa se o campo password é None e se password é diferente  de confirm_password
        #Se forem iguais, criptografa a senha
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password is None:
            return Response({'status': 400, 'msg': 'O campo Password é obrigatório!'}, status = 400)
        
        if password != confirm_password:
            return Response({'status': 409, 'msg': 'As senhas precisam ser iguais'}, status = 409)

        hashed_password = make_password(password)
        
        #Testa se nome é None
        nome = request.data.get('nome')
        if nome is None:
            return Response({'status': 400, 'msg': 'O campo nome é obrigatório!'}, status = 400)

        #Testa se o campo email é None e se email já está sendo utilizado
        email = request.data.get('email')
        if email is None:
            return Response({'status': 400, 'msg': 'O campo email é obrigatório!'}, status = 400)
        email_exist = Usuario.objects.filter(email = email).exists()
        if email_exist:
            return Response({'status': 409, 'msg': 'Email já está em uso'})
        
        #Telefone é opcional, então não verifico nada
        tel = request.data.get('telefone')
        
        #Testa se pais é None e se aquele pais existe
        pais= request.data.get('pais')
        if pais is None:
            return Response({'status': 400, 'msg': 'O campo pais é obrigatório!'}, status = 400)
        pais = Pais.objects.filter(id = pais)
        if not pais.exists():
            return Response({'status': 404, 'msg': "Pais não encontrado"}, status= 404)
        
        #Descricao também é opcional, então não verifico nada
        descricao = request.data.get('descricao')
        
        #Testa se is private é None e se não é um boleano, se for, atribui falso a ele
        is_private = request.data.get('is_private')
        if is_private is None or not isinstance(is_private, bool):
            is_private = False

        
        #Recebe os generos como lista, se for algo diferente considera como None
        generos_favoritos = request.data.get('generos_favoritos', None)
        
        if generos_favoritos is not None:
            #Testa se é uma lista
            if not isinstance(generos_favoritos, list):
                return Response({'status': 400, 'msg': "O campo generos_favoritos deve ser uma lista."}, status=400)
    
            #Retira repetidos
            generos_favoritos = list(set(generos_favoritos))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_favoritos:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first())    

        #Chegando aqui não tendo retornado nenhum erro, podemos fazer criar o Usuário
        usuario = Usuario.objects.create(
                    username=username, 
                    password=hashed_password, 
                    email=email, nome=nome, 
                    descricao=descricao,
                    telefone=tel, 
                    pais = pais.first(),
                    is_private = is_private
                    )
        
        #Se não for none, vai criar os generos_favoritos do usuário na tabela genero_usuario
        if generos_favoritos is not None:
            for genero in generos_id:
                usuario.generos_favoritos.add(genero)
            

        
        usuario.save()
        return Response({'status': 201, 'msg': 'registered successfully'})
        
#Lista todos os usuários    
class ListUsuarioView(APIView):

    def get(self, request):
        usuario = Usuario.objects.all()
        serial = UsernameSerializer(usuario, many = True)
        if len(serial.data) > 0:  
            return Response({'status': 200, 'Usuarios': serial.data},status=200)

        return Response({'status': 204, 'msg': 'No Content'}, status=204)

#Informações Especifica sobre um único usuário
class UsuarioEspecificoView(APIView):

    def get(self, request, usuario_id):
        usuario = Usuario.objects.filter(id = usuario_id)
        
        if not usuario.exists():
            return Response({'status': 404, 'msg': "Usuário não encontrado"}, status= 404)
        
        usuario = usuario.first()
        #Se o usuário for privado, vai retornar coisas diferentes
        if usuario.is_private:
            serial = UsernameSerializer(usuario, many=False)
        else:    
            serial = UsuarioSerializer(usuario, many=False)
        return Response({'status': 200, 'Usuario': serial.data},status=200)

#Informações, Modificações de si mesmo e excluir conta
class UsuarioView(APIView):

    #Autorizações: Se é está autenticado
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    #informações sobre si mesmo
    def get(self, request):
        usuario = request.user
        serial = EuSerializer(usuario)
        return Response({'status': 200, 'Usuario': serial.data},status=200)

    
    def delete(self, request):
        usuario = request.user
        autor_delete = request.data.get('autor_delete')
        if usuario.is_autor and autor_delete is True:
            autor = usuario.autor
            autor.delete()

        usuario.delete()
        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)

    def patch(self, request):
        usuario = request.user

        #Altera o username se pedido
        username = request.data.get('username')
        if username is not None:
            #Testa se já não estão usando esse username novo
            user_exists = Usuario.objects.filter(username=username).exists()
            if user_exists:
                return Response({'status': 409, 'msg': 'Username já existente!'})
            
            usuario.username= username

        #Altera a senha se pedido
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password is not None and confirm_password is not None:
            #Testa se são iguais
            if password != confirm_password:
                return Response({'status': 409, 'msg': 'As senhas precisam ser iguais'}, status = 409)

            hashed_password = make_password(password)
            usuario.password = hashed_password

        #Altera o nome se pedido
        nome = request.data.get('nome')
        if nome is not None:
            usuario.nome = nome
        
        #Altera o campo de email se pedido
        email = request.data.get('email')
        if email is not None:

            email_exist = Usuario.objects.filter(email = email).exists()
            if email_exist:
                return Response({'status': 409, 'msg': 'Email já está em uso'})
            
            usuario.email = email
        
        #Altera o telefone se pedido
        tel = request.data.get('telefone')
        if tel is not None:
            usuario.telefone = tel
        
        #Altera descricao se pedido
        descricao = request.data.get('descricao')
        if descricao is not None:
            usuario.descricao = descricao
        
        #Altera se o usuário é privado ou não, se pedido
        is_private = request.data.get('is_private')
        if is_private is not None:
            #Testa se o que foi recebido é um boleano mesmo
            if not isinstance(is_private, bool):
                return Response ({'status': 400, 'msg': 'is_private precisa ser true ou false'}, status = 400)
            
            usuario.is_private = is_private
        
        #Altera os generos favoritos se pedido
        generos_favoritos = request.data.get('generos_favoritos', None)

        if generos_favoritos is not None:
            #Testa se é uma lista
            if not isinstance(generos_favoritos, list):
                return Response({'status': 400, 'msg': "O campo generos_favoritos deve ser uma lista."}, status=400)
    
            #Retira repetidos
            generos_favoritos = list(set(generos_favoritos))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_favoritos:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first()) 

            usuario.generos_favoritos.set(generos_id)

        #Por ultimo, salva as alterações
        usuario.save()
        return Response({'status': 200, 'msg': 'Alterado com SUCESSO'}, status = 200)










