from django.urls import path
from .views import ListaStatusView, UsuarioStatusView, ListaStatusLivroView, UsuarioDeletaStatusView

urlpatterns = [
    path('Usuario/<int:usuario_id>/Livros/<int:status>/', ListaStatusView.as_view()),
    path('Usuario/me/Status/<int:status>/Livro/<int:livro_id>/', UsuarioStatusView.as_view()),
    path('Usuario/me/Status/<int:status>/Livro/', UsuarioStatusView.as_view()),
    path('Usuario/me/Status/delete/Livro/<int:livro_id>/', UsuarioDeletaStatusView.as_view()),
    path('Livro/<int:livro_id>/Status/<int:status>/', ListaStatusLivroView.as_view()),
]