from rest_framework.views import APIView

from .models import Livro
from .serializer import LivroSerializerDetaield, LivroSerializer
from Autor.models import Autor
from rest_framework.response import Response
from django.http import JsonResponse
from Genero.models import Genero

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class UsuarioLivroView(APIView):

    #Autorizações: Se é está autenticado
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):

        usuario = request.user
        if not usuario.is_autor:
            return Response({'status': 400, 'msg': 'O usuário não tem um autor atribuido a ele!'}, status = 400)
        
        titulo = request.data.get('titulo')
        if titulo is None:
            return Response({'status': 400, 'msg': 'O campo titulo é obrigatório!'}, status = 400)
        
        descricao = request.data.get('descricao')
        if descricao is None:
            return Response({'status': 400, 'msg': 'O campo descricao é obrigatório!'}, status = 400)
        
        data_publicacao = request.data.get('data_publicacao')
        if data_publicacao is None:
            return Response({'status': 400, 'msg': 'O campo data_publicacao é obrigatório!'}, status = 400)
        
        n_paginas = request.data.get('n_paginas')
        if n_paginas is None:
            return Response({'status': 400, 'msg': 'O campo n_paginas é obrigatório!'}, status = 400)
        
        autor = usuario.autor

        generos_livro = request.data.get('generos_livro', None)
        
        if generos_livro is not None:
            #Testa se é uma lista
            if not isinstance(generos_livro, list):
                return Response({'status': 400, 'msg': "O campo generos_livro deve ser uma lista."}, status=400)
    
            #Retira repetidos
            generos_livro = list(set(generos_livro))

            generos_id = []
            #Para cada genero, testa se ele existe. Se não, informa o erro
            for genero in generos_livro:
                genero = Genero.objects.filter(id = genero)
                if not genero.exists():
                    return Response ({'status': 404, 'msg': "Genero não encontrado"}, status= 404)
                generos_id.append(genero.first())

        livro = Livro.objects.create(titulo=titulo,descricao=descricao,data_publicacao=data_publicacao,n_paginas=n_paginas,autor=autor) 

        if generos_livro is not None:
            for genero in generos_id:
                livro.generos_livro.add(genero) 

        autor.save()
        return Response({'status': 201, 'msg': 'registered successfully'})
    

    def delete(self, request, pk):

        usuario = request.user
        if not usuario.is_autor:
            return Response({'status': 400, 'msg': 'O usuário não tem um autor atribuido a ele!'}, status = 400)
        
        livro = Livro.objects.filter(id=pk)
        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)

        livro = livro.first()
        if livro.autor != usuario.autor:
            return Response({'status': 401, 'msg': 'Livro não pertence ao Usuário'}, status = 401)
        
        livro.delete()
        return Response({'status': 200, 'msg': 'Deletado com SUCESSO'}, status = 200)
    
    def patch(self, request, pk):

        usuario = request.user
        if not usuario.is_autor:
            return Response({'status': 400, 'msg': 'O usuário não tem um autor atribuido a ele!'}, status = 400)
        
        livro = Livro.objects.filter(id=pk)
        if not livro.exists():
            return Response({'status': 404, 'msg': 'Livro não encontrado'}, status = 404)

        livro = livro.first()
        if livro.autor != usuario.autor:
            return Response({'status': 401, 'msg': 'Livro não pertence ao Usuário'}, status = 401)
        
        titulo = request.data.get('titulo')
        if titulo is not None:
            livro.titulo = titulo
        
        descricao = request.data.get('descricao')
        if descricao is not None:
            livro.descricao = descricao

        data_publicacao = request.data.get('data_publicacao')
        if data_publicacao is not None:
            livro.data_publicacao = data_publicacao
        
        n_paginas = request.data.get('n_paginas')
        if n_paginas is not None:
            livro.n_paginas = n_paginas

        livro.save()
        return Response({'status': 200, 'msg': 'Alterado com SUCESSO'}, status = 200)

class ListaLivrosView(APIView):
    def get(self, request):
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        if len(serializer.data) > 0:
            return Response({
                'status': 302,
                'Livros': serializer.data
            })
        return Response({'status': 204, 'msg': 'No Content'})

class DetailedLivroView(APIView):
    def get(self, request, pk=None):  
        if pk is not None:  
            try:
                livro = Livro.objects.get(pk=pk)
                serializer = LivroSerializerDetaield(livro)
                return Response({
                    'status': 302,
                    'Livro': serializer.data
                })
            except Livro.DoesNotExist:
                return Response({'status': 404, 'msg': 'Livro não encontrado'})
        else:
            return Response({'status': 404, 'msg': 'ID do livro não fornecido'})

class ListaLivrosAutorView(APIView):
    def get(self, request, autor_id=None):
        if autor_id is not None:  
            try:
                autor = Autor.objects.get(pk=autor_id) 
                livros = Livro.objects.filter(autor=autor)  
                serializer = LivroSerializer(livros, many=True)
                if len(serializer.data) > 0:
                    return Response({
                        'status': 302,
                        'Livros': serializer.data
                    })
                else:
                    return Response({'status': 204, 'msg': 'No Content'})
            except Autor.DoesNotExist:
                return Response({'status': 404, 'msg': 'Autor não encontrado'})
        else:
            return Response({'status': 404, 'msg': 'ID do autor não fornecido'})


