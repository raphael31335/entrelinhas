# livros/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro, LivroUsuario
from .forms import LivroForm
from .utils import buscar_livros_api, gerar_sugestoes


@login_required
def minha_estante(request):
    # Agora filtra por LivroUsuario, não Livro
    relacoes_livros = LivroUsuario.objects.filter(user=request.user)
    return render(request, 'livros/minha_estante.html', {'relacoes_livros': relacoes_livros})


@login_required
def buscar_livros(request):
    resultados = []
    if 'q' in request.GET:
        termo = request.GET.get('q')
        resultados = buscar_livros_api(termo)
    return render(request, 'livros/buscar.html', {'livros': resultados})


@login_required
def salvar_livro_api(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autores = request.POST.get('autores')
        google_id = request.POST.get('google_id')
        capa = request.POST.get('capa')

        try:
            # Passo 1: Encontra ou cria o livro genérico
            livro_generico, livro_criado = Livro.objects.get_or_create(
                google_id=google_id,
                defaults={
                    'titulo': titulo,
                    'autores': autores,
                    'capa': capa
                }
            )

            # Passo 2: Encontra ou cria a relação entre o usuário e o livro
            relacao, relacao_criada = LivroUsuario.objects.get_or_create(
                user=request.user,
                livro=livro_generico
            )

            if relacao_criada:
                messages.success(request, f'O livro "{livro_generico.titulo}" foi adicionado à sua estante!')
            else:
                messages.warning(request, f'O livro "{livro_generico.titulo}" já está na sua estante.')
        
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao salvar o livro: {e}')

        return redirect('minha_estante')

    return redirect('minha_estante')


@login_required
def cadastro_manual(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            # A lógica aqui agora cria um Livro genérico primeiro
            novo_livro = form.save()
            # E depois cria a relação com o usuário
            LivroUsuario.objects.create(user=request.user, livro=novo_livro)
            messages.success(request, 'Livro cadastrado manualmente!')
            return redirect('minha_estante')
    else:
        form = LivroForm()
    return render(request, 'livros/cadastro_manual.html', {'form': form})


@login_required
def editar_livro(request, livro_usuario_id):
    # Encontra a relação LivroUsuario para o usuário logado
    relacao = get_object_or_404(LivroUsuario, id=livro_usuario_id, user=request.user)
    
    # O formulário agora lida com os campos do LivroUsuario
    # Você precisará criar um LivroUsuarioForm ou usar um modelo de formulário simples
    if request.method == 'POST':
        # Exemplo de como salvar os campos do LivroUsuario
        relacao.status = request.POST.get('status')
        relacao.nota = request.POST.get('nota')
        relacao.comentario = request.POST.get('comentario')
        relacao.data_leitura = request.POST.get('data_leitura')
        relacao.save()
        
        messages.success(request, 'Livro atualizado com sucesso!')
        return redirect('minha_estante')
    else:
        return render(request, 'livros/editar.html', {'relacao': relacao})


@login_required
def remover_livro(request, livro_usuario_id):
    # Encontra e deleta a relação LivroUsuario, não o livro genérico
    relacao = get_object_or_404(LivroUsuario, id=livro_usuario_id, user=request.user)
    relacao.delete()
    messages.success(request, 'Livro removido da sua estante.')
    return redirect('minha_estante')


@login_required
def sugestoes_para_mim(request):
    sugestoes = gerar_sugestoes(request.user)
    return render(request, 'livros/sugestoes.html', {'sugestoes': sugestoes})
