from django.urls import path
from .views import UsuarioLidoView, UsuarioLendoView, UsuarioQuerLerView, UsuarioDeletaStatusView, ListaLidosUsuarioView, ListaLendoUsuarioView, ListaQuerLerUsuarioView
urlpatterns = [
    path('Usuario/<int:usuario_id>/Livros/Status/Lidos/', ListaLidosUsuarioView.as_view()),
    path('Usuario/<int:usuario_id>/Livros/Status/Lendo/', ListaLendoUsuarioView.as_view()),
    path('Usuario/<int:usuario_id>/Livros/Status/QuerLer/', ListaQuerLerUsuarioView.as_view()),
    path('Usuario/me/Livros/Status/Lidos/', UsuarioLidoView.as_view()),
    path('Usuario/me/Livros/Status/Lidos/<int:livro_id>/', UsuarioLidoView.as_view()),
    path('Usuario/me/Livros/Status/Lendo/', UsuarioLendoView.as_view()),
    path('Usuario/me/Livros/Status/Lendo/<int:livro_id>/', UsuarioLendoView.as_view()),
    path('Usuario/me/Livros/Status/QuerLer/', UsuarioQuerLerView.as_view()),
    path('Usuario/me/Livros/Status/QuerLer/<int:livro_id>/', UsuarioQuerLerView.as_view()),
    path('Usuario/me/Livros/Status/Delete/<int:livro_id>/', UsuarioDeletaStatusView.as_view()),
]