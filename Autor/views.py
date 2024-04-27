from rest_framework.views import APIView
from .models import Autor
from .serializer import AutorSerializerDetaield,ListaAutoresSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from Genero.models import Genero
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from Usuario.models import Usuario

#Atribui um autor a um usuário
class StaffAtribuiAutorView(APIView):
    #Autorizações: Se é está autenticado e se é Staff
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    
    def patch(self, request, usuario_id, autor_id):
        #Testa se esse usuario existe
        usuario = Usuario.objects.filter(id = usuario_id)
        if not usuario.exists():
            return Response({'status': 404, 'msg': 'usuario não encontrado!'}, status = 404)
                
        usuario = usuario.first()

        #Testa se esse autor existe
        autor = Autor.objects.filter(id = autor_id)
        if not autor.exists():
            return Response({'status': 404, 'msg': 'Autor não encontrado!'}, status = 404)
        
        autor = autor.first()

        #Testa se existe um usuário atribuido a esse autor
        #Se houver, retira essa atribuição para atribuir no usuario desejado
        usuario_autor = Usuario.objects.filter(autor = autor)

        if usuario_autor.exists():
            usuario_autor = usuario_autor.first()
            usuario_autor.autor = None
            usuario_autor.is_autor = False
            usuario_autor.save()


        usuario.autor = autor
        usuario.is_autor = True
        usuario.save()
        return Response({'status': 200, 'msg': 'Atribuido com SUCESSO'}, status = 200)

#Cria, Altera e Deleta autores
class StaffAutorView(APIView):

    #Autorizações: Se é está autenticado e se é Staff
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):  
        #Testa se foi informado nome, pois nome é um campo obrigatório
        nome = request.data.get('nome')
        if nome is None:
            return Response({'status': 400, 'msg': 'O campo nome é obrigatório!'}, status = 400)

        #Descricao não é um campo obrigatório, então nada é testado
        descricao = request.data.get('descricao')
        
        #Testa se foi informado data de nascimento, pois é um campo obrigatório
        born_in = request.data.get('born_in')
        if born_in is None:
            return Response({'status': 400, 'msg': 'O campo born_in é obrigatório!'}, status = 400)
        
        #Não testa nada pois a data de morte é opcional
        died_in = request.data.get('died_in')
        
        generos_autor = request.data.get('generos_autor', None)
        
        if generos_autor is not None:
            #Testa se é uma lista
            if not isinstance(generos_autor, list):
                return Response({'status': 400, 'msg': "O campo generos_autor deve ser uma lista."}, status=400)

            #Retira repetidos
            generos_autor = list(set(generos_autor))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_autor:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first())    

        autor = Autor.objects.create(nome=nome,descricao=descricao,born_in=born_in,died_in=died_in)  

        if generos_autor is not None:
            for genero in generos_id:
                autor.generos_autor.add(genero)
        
        autor.save()
        return Response({'status': 201, 'msg': 'registered successfully'})
    
    def delete(self, request, autor_id):

        autor = Autor.objects.filter(id = autor_id)
        if not autor.exists():
            return Response({'status': 404, 'msg': 'Autor não encontrado!'}, status = 404)
        
        autor = autor.first()

        #Se esse autor estiver atrelado a um usuário, temos que colocar  is_autor pra False
        usuario = Usuario.objects.filter(autor = autor)

        if usuario.exists():
            usuario = usuario.first()
            usuario.is_autor = False
            usuario.save()
        
        autor.delete()
        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)

    def patch(self, request, autor_id):

        autor = Autor.objects.filter(id = autor_id)
        if not autor.exists():
            return Response({'status': 404, 'msg': 'Autor não encontrado!'}, status = 404)
        
        autor = autor.first()
        
        #Atualiza o nome se pedido
        nome = request.data.get('nome')
        if nome is not None:
            autor.nome = nome

        #Atualiza a descrição se pedido
        descricao = request.data.get('descricao')
        if descricao is not None:
            autor.descricao = descricao

        #Atualiza o born_in se pedido
        born_in = request.data.get('born_in')
        if born_in is not None:
            autor.born_in = born_in

        #Atualiza o dead_in se pedido
        died_in = request.data.get('died_in')
        if died_in is not None:
            if died_in is False:
                died_in = None
            autor.died_in = died_in

        #Atualiza os generos do autor se pedido
        generos_autor = request.data.get('generos_autor', None)
        
        if generos_autor is not None:
            #Testa se é uma lista
            if not isinstance(generos_autor, list):
                return Response({'status': 400, 'msg': "O campo generos_autor deve ser uma lista."}, status=400)
    
            #Retira repetidos
            generos_autor = list(set(generos_autor))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_autor:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first())

            autor.generos_autor.set(generos_id)

        

        autor.save()
        return Response({'status': 200, 'msg': 'Alterado com SUCESSO'}, status = 200)

#Cria, Altera e Deleta o autor de um usuário
class UsuarioAutorView(APIView):

    #Autorizações: Se é está autenticado
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def post(self, request):
        
        usuario = request.user
        #Testa se o usuário já não tem um autor atribuido a ele:
        if usuario.is_autor:
            return Response({'status': 400, 'msg': 'O usuário já tem um autor atribuido a ele!'}, status = 400)
        
        #Testa se foi informado nome, pois nome é um campo obrigatório
        nome = request.data.get('nome')
        if nome is None:
            return Response({'status': 400, 'msg': 'O campo nome é obrigatório!'}, status = 400)

        #Descricao não é um campo obrigatório, então nada é testado
        descricao = request.data.get('descricao')
        
        #Testa se foi informado data de nascimento, pois é um campo obrigatório
        born_in = request.data.get('born_in')
        if born_in is None:
            return Response({'status': 400, 'msg': 'O campo born_in é obrigatório!'}, status = 400)
        
        #Não testa nada pois a data de morte é opcional
        died_in = request.data.get('died_in')
        
        generos_autor = request.data.get('generos_autor', None)
        
        if generos_autor is not None:
            #Testa se é uma lista
            if not isinstance(generos_autor, list):
                return Response({'status': 400, 'msg': "O campo generos_autor deve ser uma lista."}, status=400)
    
            #Retira repetidos
            generos_autor = list(set(generos_autor))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_autor:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first())    
    
        autor = Autor.objects.create(nome=nome,descricao=descricao,born_in=born_in,died_in=died_in)  

        if generos_autor is not None:
            for genero in generos_id:
                autor.generos_autor.add(genero)
       
        usuario.autor = autor
        usuario.is_autor = True
        usuario.save()
        autor.save()
        return Response({'status': 201, 'msg': 'registered successfully'})
    
    def delete(self, request):
        usuario = request.user
        #Testa se usuário não é autor, pois se não for, não pode deletar
        if not usuario.is_autor:
            return Response({'status': 400, 'msg': 'O usuário não tem um autor atribuido a ele!'}, status = 400)
        
        autor = usuario.autor
        #Atualiza usuario para não deletar o usuário também quando deletar o autor
        usuario.is_autor = False
        usuario.save()
        autor.delete()

        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)

    def patch(self, request):
        
        usuario = request.user
        #Testa se o usuario não é um autor, pois ele não pode atualizar se ele não tem um autor atribuido a ele
        if not usuario.is_autor:
            return Response({'status': 400, 'msg': 'O usuário não tem um autor atribuido a ele!'}, status = 400)
        
        autor = usuario.autor
        
        #Atualiza o nome se pedido
        nome = request.data.get('nome')
        if nome is not None:
            autor.nome = nome

        #Atualiza a descrição se pedido
        descricao = request.data.get('descricao')
        if descricao is not None:
            autor.descricao = descricao

        #Atualiza o born_in se pedido
        born_in = request.data.get('born_in')
        if born_in is not None:
            autor.born_in = born_in

        #Atualiza o dead_in se pedido
        died_in = request.data.get('died_in')
        if died_in is not None:
            #Se receber que died_in é falso, atribui None a ele. Essa solução veio para após inserir o died_in(talvez por engano)
            # o usuário ainda possa tornar ele None novamente
            if died_in is False:
                died_in = None
            autor.died_in = died_in

        #Atualiza os generos do autor se pedido
        generos_autor = request.data.get('generos_autor', None)
        
        if generos_autor is not None:
            #Testa se é uma lista
            if not isinstance(generos_autor, list):
                return Response({'status': 400, 'msg': "O campo generos_autor deve ser uma lista."}, status=400)
    
            #Retira repetidos
            generos_autor = list(set(generos_autor))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_autor:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first())

            autor.generos_autor.set(generos_id)

        

        autor.save()
        return Response({'status': 200, 'msg': 'Alterado com SUCESSO'}, status = 200)
        
#Lista todos os autores
class ListaAutoresView(APIView):
    
    def get(self, request):
        autor = Autor.objects.all()
        serializer = ListaAutoresSerializer(autor, many=True)
        if len(serializer.data) > 0:
            return Response({
                'status': 302,
                'Autores': serializer.data
            })
        return Response({'status': 204, 'msg': 'No Content'})

#Lista um autor em especifico
class AutorDetailedView(APIView):
    def get(self, request, autor_id=None):  
        if autor_id is not None:  
            try:
                autor = Autor.objects.get(pk=autor_id)
                serializer = AutorSerializerDetaield(autor)
                return Response({
                    'status': 302,
                    'Autor': serializer.data
                })
            except Autor.DoesNotExist:
                return Response({'status': 404, 'msg': 'Autor não encontrado'}, status=404)
        else:
            return Response({'status': 404, 'msg': 'ID do Autor não fornecido'}, status = 404)
        