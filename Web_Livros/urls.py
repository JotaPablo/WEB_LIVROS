
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', views.obtain_auth_token),
    path('', include(router.urls)),
    path('', include('Pais.urls')),
    path('', include('Genero.urls')),
    path('', include('Usuario.urls')),
    path('', include('Autor.urls')),
    path('', include('Livro.urls')),
    path('', include('Avaliacao.urls')),
    path('', include('Status_Livro.urls'))
]
