from django.urls import path
from . import views

urlpatterns = [
    path('estante/', views.minha_estante, name='minha_estante'),
    path('buscar/', views.buscar_livros, name='buscar_livros'),
    path('salvar/', views.salvar_livro, name='salvar_livro'),
    path('manual/', views.cadastro_manual, name='cadastro_manual'),
    path('remover/<int:pk>/', views.remover_livro, name='remover_livro'),
    path('editar/<int:pk>/', views.editar_livro, name='editar_livro'),
]
