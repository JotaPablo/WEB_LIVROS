from django.urls import path
from .views import UsuarioLivroView, ListaLivrosView, ListaLivrosAutorView, DetailedLivroView

urlpatterns = [
    path('Usuario/me/Livro/', UsuarioLivroView.as_view()),
    path('Usuario/me/Livro/<int:pk>/', UsuarioLivroView.as_view()),
    path('Livros/', ListaLivrosView.as_view()),
    path('Livros/<int:pk>/', DetailedLivroView.as_view()),
    path('Autores/<int:autor_id>/Livros', ListaLivrosAutorView.as_view()),
]