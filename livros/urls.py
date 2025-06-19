from django.urls import path
from . import views

urlpatterns = [
    path('minha-estante/', views.minha_estante, name='minha_estante'),
    path('buscar/', views.buscar_livros, name='buscar_livros'),
    path('salvar/', views.salvar_livro_api, name='salvar_livro_api'),
    path('cadastro-manual/', views.cadastro_manual, name='cadastro_manual'),
    path('editar/<int:livro_id>/', views.editar_livro, name='editar_livro'),
    path('remover/<int:livro_id>/', views.remover_livro, name='remover_livro'),
    path('sugestoes/', views.sugestoes_para_mim, name='sugestoes_para_mim'),
]
