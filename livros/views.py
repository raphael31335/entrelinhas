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

        if not Livro.objects.filter(user=request.user, google_id=google_id).exists():
            livro = Livro(
                user=request.user,
                titulo=titulo,
                autores=autores,
                google_id=google_id,
                capa=capa
            )
            livro.save()
            messages.success(request, 'Livro salvo na sua estante!')
        else:
            messages.warning(request, 'Este livro já está na sua estante.')

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