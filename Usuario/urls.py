from django.urls import path
from .views import RegisterView, ListUsuarioView, UsuarioEspecificoView, UsuarioView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('Usuario/' , ListUsuarioView.as_view()),
    path('Usuario/<int:usuario_id>/', UsuarioEspecificoView.as_view()),
    path('Usuario/me/', UsuarioView.as_view())
]