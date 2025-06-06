# livros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro
from .forms import LivroForm
from django.contrib.auth.decorators import login_required
import requests

@login_required
def minha_estante(request):
    livros = Livro.objects.filter(user=request.user)
    return render(request, 'livros/estante.html', {'livros': livros})

@login_required
def buscar_livros(request):
    query = request.GET.get('q')
    livros = []
    if query:
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
        if response.status_code == 200:
            data = response.json()
            livros = [
                {
                    'google_id': item['id'],
                    'titulo': item['volumeInfo'].get('title'),
                    'autores': ', '.join(item['volumeInfo'].get('authors', [])),
                    'capa': item['volumeInfo'].get('imageLinks', {}).get('thumbnail')
                }
                for item in data.get('items', [])
            ]
    return render(request, 'livros/buscar.html', {'livros': livros})

@login_required
def salvar_livro(request):
    if request.method == 'POST':
        google_id = request.POST.get('google_id')
        if not Livro.objects.filter(user=request.user, google_id=google_id).exists():
            livro = Livro(
                user=request.user,
                google_id=google_id,
                titulo=request.POST.get('titulo'),
                autores=request.POST.get('autores'),
                capa=request.POST.get('capa'),
            )
            livro.save()
        return redirect('minha_estante')
    return redirect('buscar_livros')

@login_required
def cadastro_manual(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.user = request.user
            livro.save()
            return redirect('minha_estante')
    else:
        form = LivroForm()
    return render(request, 'livros/cadastro_manual.html', {'form': form})

@login_required
def remover_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk, user=request.user)
    livro.delete()
    return redirect('minha_estante')

@login_required
def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('minha_estante')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/editar.html', {'form': form})
