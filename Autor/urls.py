from django.urls import path
from .views import UsuarioAutorView, ListaAutoresView, AutorDetailedView, StaffAutorView, StaffAtribuiAutorView

urlpatterns = [
    path('Usuario/me/Autor/', UsuarioAutorView.as_view()),
    path('Autores/', ListaAutoresView.as_view() ),
    path('Autores/<int:autor_id>/', AutorDetailedView.as_view()),
    path('Staff/Autor/', StaffAutorView.as_view()),
    path('Staff/Autor/<int:autor_id>/', StaffAutorView.as_view()),
    path('Staff/Usuario/<int:usuario_id>/Autor/<int:autor_id>/', StaffAtribuiAutorView.as_view())

]