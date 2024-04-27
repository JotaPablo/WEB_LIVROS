from django.urls import path
from .views import RegisterView, ListUsuarioView, UsuarioEspecificoView, UsuarioView, StaffUsuarioView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('Usuario/' , ListUsuarioView.as_view()),
    path('Usuario/<int:usuario_id>/', UsuarioEspecificoView.as_view()),
    path('Usuario/me/', UsuarioView.as_view()),
    path('Staff/Usuario/<int:usuario_id>/', StaffUsuarioView.as_view())

]