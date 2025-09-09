# No arquivo: livros/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro
from .forms import LivroForm
from .utils import buscar_livros_api, gerar_sugestoes


@login_required
def minha_estante(request):
    livros = Livro.objects.filter(user=request.user)
    return render(request, 'livros/minha_estante.html', {'livros': livros})


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

        # 1. Tenta encontrar o livro pelo google_id.
        #    Se não existir, ele cria um novo com os dados fornecidos.
        livro, criado = Livro.objects.get_or_create(
            google_id=google_id,
            defaults={
                'titulo': titulo,
                'autores': autores,
                'capa': capa
            }
        )

        # 2. Verifica se o livro já está associado ao usuário atual.
        #    Se não estiver, o associa.
        if Livro.objects.filter(user=request.user, google_id=google_id).exists():
            messages.warning(request, f'O livro "{livro.titulo}" já está na sua estante.')
        else:
            livro.user = request.user
            livro.save()
            if criado:
                messages.success(request, f'O livro "{livro.titulo}" foi salvo na base de dados e adicionado à sua estante!')
            else:
                messages.success(request, f'O livro "{livro.titulo}" já existe. Adicionado à sua estante.')
        
        return redirect('minha_estante')
    
    return redirect('minha_estante')


@login_required
def cadastro_manual(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.user = request.user
            livro.save()
            messages.success(request, 'Livro cadastrado manualmente!')
            return redirect('minha_estante')
    else:
        form = LivroForm()
    return render(request, 'livros/cadastro_manual.html', {'form': form})


@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id, user=request.user)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('minha_estante')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/editar.html', {'form': form})


@login_required
def remover_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id, user=request.user)
    livro.delete()
    messages.success(request, 'Livro removido da sua estante.')
    return redirect('minha_estante')


@login_required
def sugestoes_para_mim(request):
    sugestoes = gerar_sugestoes(request.user)
    return render(request, 'livros/sugestoes.html', {'sugestoes': sugestoes})
