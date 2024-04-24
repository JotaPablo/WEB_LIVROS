from django.urls import path
from .views import AvaliacaoCreateAPIView, ComentarioCreateAPIView, AvaliacaoListAPIView,ComentariosListAPIView, StaffDeletaAvalaiacao, StaffDeletaComentario

urlpatterns = [
    path('Avaliacoes/create/', AvaliacaoCreateAPIView.as_view(), name='avaliacao-create'),
    path('Avaliacoes/delete/<int:avaliacao_id>/', AvaliacaoCreateAPIView.as_view(), name='avaliacao-delete'),
    path('Comentarios/create/', ComentarioCreateAPIView.as_view(), name='comentario-create'),
    path('Comentarios/delete/<int:comentario_id>/', ComentarioCreateAPIView.as_view(), name='comentario-delete'),
    path('Avaliacoes/<int:livro_id>/',AvaliacaoListAPIView.as_view(),name = 'avaliacoes-list'),
    path('Comentarios/<int:avaliacao_id>/',ComentariosListAPIView.as_view(),name = 'comentarios-list'),
    path('Staff/Avaliacao/<int:avaliacao_id>/', StaffDeletaAvalaiacao.as_view()),
    path('Staff/Comentario/<int:comentario_id>/', StaffDeletaComentario.as_view())
]