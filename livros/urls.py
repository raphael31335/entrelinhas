# livros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.minha_estante, name='minha_estante'),
    path('buscar/', views.buscar_livros, name='buscar_livros'),
    path('salvar/', views.salvar_livro_api, name='salvar_livro_api'),
    path('cadastro/', views.cadastro_manual, name='cadastro_manual'),
    path('editar/<int:livro_usuario_id>/', views.editar_livro, name='editar_livro'),
    path('remover/<int:livro_usuario_id>/', views.remover_livro, name='remover_livro'),
    path('sugestoes/', views.sugestoes_para_mim, name='sugestoes_para_mim'),

    # rota de debug - REMOVA quando finalizar
    path('debug/db_status/', views.debug_db_status, name='debug_db_status'),
]
