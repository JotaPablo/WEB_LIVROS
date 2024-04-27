from django.urls import path
from .views import UsuarioLivroView, ListaLivrosView, ListaLivrosAutorView, DetailedLivroView, StaffLivroView

urlpatterns = [
    path('Staff/Livro/', StaffLivroView.as_view()),
    path('Staff/Livro/<int:livro_id>/', StaffLivroView.as_view()),
    path('Usuario/me/Livro/', UsuarioLivroView.as_view()),
    path('Usuario/me/Livro/<int:livro_id>/', UsuarioLivroView.as_view()),
    path('Livros/', ListaLivrosView.as_view()),
    path('Livros/<int:pk>/', DetailedLivroView.as_view()),
    path('Autores/<int:autor_id>/Livros', ListaLivrosAutorView.as_view()),
]