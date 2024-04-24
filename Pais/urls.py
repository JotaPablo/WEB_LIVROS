from django.urls import path
from .views import ListPaisView, StaffPaisView, UsuarioPaisView

urlpatterns = [
    path('Pais/<int:pais_id>/', UsuarioPaisView.as_view()),
    path('Staff/Pais/', StaffPaisView.as_view()),
    path('Staff/Pais/<int:pais_id>/', StaffPaisView.as_view()),
    path('Pais/', ListPaisView.as_view()),
]