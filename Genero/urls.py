from django.urls import path
from .views import ListGeneroView, StaffGeneroView, ListUsuarioPorGeneroView, ListAutoresPorGeneroView, ListLivrosPorGeneroView

urlpatterns = [
    path('Staff/Genero/', StaffGeneroView.as_view()),
    path('Staff/Genero/<int:genero_id>/', StaffGeneroView.as_view()),
    path('Genero/', ListGeneroView.as_view()),
    path('Genero/<int:genero_id>/Usuario/', ListUsuarioPorGeneroView.as_view()),
    path('Genero/<int:genero_id>/Livro/', ListLivrosPorGeneroView.as_view()),
    path('Genero/<int:genero_id>/Autor/', ListAutoresPorGeneroView.as_view()),
]