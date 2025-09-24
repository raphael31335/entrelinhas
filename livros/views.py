import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Livro, LivroUsuario
from .forms import LivroUsuarioForm


# Página inicial
def home(request):
    return render(request, "home.html")


# Buscar livros pela API do Google Books
@login_required
def buscar_livros(request):
    livros = []
    query = request.GET.get("q")
    if query:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                livros.append({
                    "google_id": item.get("id"),
                    "titulo": volume_info.get("title"),
                    "autores": ", ".join(volume_info.get("authors", [])),
                    "descricao": volume_info.get("description", ""),
                    "capa_url": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                })
    return render(request, "buscar.html", {"livros": livros})


# Salvar livro na estante do usuário
@login_required
def salvar_livro(request, google_id):
    livro, created = Livro.objects.get_or_create(
        google_id=google_id,
        defaults={
            "titulo": request.POST.get("titulo"),
            "autores": request.POST.get("autores"),
            "descricao": request.POST.get("descricao"),
            "capa_url": request.POST.get("capa_url"),
        }
    )

    try:
        LivroUsuario.objects.create(user=request.user, livro=livro)
        messages.success(request, "Livro salvo com sucesso na sua estante!")
    except:
        messages.warning(request, "Você já salvou este livro.")

    return redirect("minha_estante")


# Minha estante (livros salvos pelo usuário)
@login_required
def minha_estante(request):
    livros_usuario = LivroUsuario.objects.filter(user=request.user)
    return render(request, "minha_estante.html", {"livros_usuario": livros_usuario})


# Editar livro da estante
@login_required
def editar_livro_usuario(request, pk):
    livro_usuario = get_object_or_404(LivroUsuario, pk=pk, user=request.user)
    if request.method == "POST":
        form = LivroUsuarioForm(request.POST, instance=livro_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect("minha_estante")
    else:
        form = LivroUsuarioForm(instance=livro_usuario)
    return render(request, "editar_livro.html", {"form": form})


# Remover livro da estante
@login_required
def remover_livro_usuario(request, pk):
    livro_usuario = get_object_or_404(LivroUsuario, pk=pk, user=request.user)
    livro_usuario.delete()
    messages.success(request, "Livro removido da sua estante.")
    return redirect("minha_estante")


# Cadastro manual de livros
@login_required
def cadastro_manual(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        autores = request.POST.get("autores")
        descricao = request.POST.get("descricao")
        capa_url = request.POST.get("capa_url")

        livro, created = Livro.objects.get_or_create(
            titulo=titulo,
            autores=autores,
            descricao=descricao,
            capa_url=capa_url,
        )

        LivroUsuario.objects.get_or_create(user=request.user, livro=livro)
        messages.success(request, "Livro cadastrado manualmente na sua estante!")
        return redirect("minha_estante")

    return render(request, "cadastro_manual.html")


# Sugestões para o usuário (IA simples baseada em autor e status)
@login_required
def sugestoes_para_mim(request):
    # Pegando livros que o usuário já tem
    meus_livros = LivroUsuario.objects.filter(user=request.user)
    autores_lidos = set(livro.livro.autores for livro in meus_livros if livro.livro.autores)

    # Sugerindo livros do mesmo autor que não estão na estante
    sugestoes = Livro.objects.exclude(livrousuario__user=request.user)
    if autores_lidos:
        sugestoes = sugestoes.filter(autores__in=autores_lidos)

    return render(request, "sugestoes.html", {"sugestoes": sugestoes})
