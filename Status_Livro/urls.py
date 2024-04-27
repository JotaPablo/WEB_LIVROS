from django.urls import path
from .views import UsuarioLidoView, UsuarioLendoView, UsuarioQuerLerView, UsuarioDeletaStatusView, ListaLidosUsuarioView, ListaLendoUsuarioView, ListaQuerLerUsuarioView
from .views import ListaLidosLivroView, ListaQuerLerLivroView, ListaLendoLivroView
urlpatterns = [
    path('Usuario/<int:usuario_id>/Livros/Lidos/', ListaLidosUsuarioView.as_view()),
    path('Usuario/<int:usuario_id>/Livros/Lendo/', ListaLendoUsuarioView.as_view()),
    path('Usuario/<int:usuario_id>/Livros/QuerLer/', ListaQuerLerUsuarioView.as_view()),
    path('Usuario/me/Livros/Lidos/', UsuarioLidoView.as_view()),
    path('Usuario/me/Livros/Lidos/<int:livro_id>/', UsuarioLidoView.as_view()),
    path('Usuario/me/Livros/Lendo/', UsuarioLendoView.as_view()),
    path('Usuario/me/Livros/Lendo/<int:livro_id>/', UsuarioLendoView.as_view()),
    path('Usuario/me/Livros/QuerLer/', UsuarioQuerLerView.as_view()),
    path('Usuario/me/Livros/QuerLer/<int:livro_id>/', UsuarioQuerLerView.as_view()),
    path('Usuario/me/Livros/Status/Delete/<int:livro_id>/', UsuarioDeletaStatusView.as_view()),
    path('Livros/<int:livro_id>/Lidos/', ListaLidosLivroView.as_view()),
    path('Livros/<int:livro_id>/Lendo/', ListaLendoLivroView.as_view()),
    path('Livros/<int:livro_id>/QuerLer/', ListaQuerLerLivroView.as_view()),
]