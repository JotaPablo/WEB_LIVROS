from django.urls import path
from .views import UsuarioAutorView, ListaAutoresView, AutorDetailedView, StaffAutorView

urlpatterns = [
    path('Usuario/me/Autor/', UsuarioAutorView.as_view()),
    path('Autores/', ListaAutoresView.as_view() ),
    path('Autores/<int:pk>/', AutorDetailedView.as_view()),
    path('Staff/Autor/', StaffAutorView.as_view()),
    path('Staff/Autor/<int:autor_id>/', StaffAutorView.as_view()),
    #hello
]