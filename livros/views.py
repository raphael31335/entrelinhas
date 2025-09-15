from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro, LivroUsuario
from .forms import LivroForm
from .utils import buscar_livros_api, gerar_sugestoes
from django.db import IntegrityError, transaction

@login_required
def minha_estante(request):
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
        google_id = request.POST.get('google_id') or None
        capa = request.POST.get('capa')

        try:
            # Garante atomicidade: evitar race conditions
            with transaction.atomic():
                livro_generico, created = Livro.objects.get_or_create(
                    google_id=google_id,
                    defaults={'titulo': titulo, 'autores': autores, 'capa': capa}
                )
                relacao, rel_created = LivroUsuario.objects.get_or_create(
                    user=request.user,
                    livro=livro_generico
                )

            if rel_created:
                messages.success(request, f'Livro "{livro_generico.titulo}" salvo na sua estante!')
            else:
                messages.warning(request, 'Este livro já está na sua estante.')

        except IntegrityError:
            # Em caso de concorrência onde o livro acabou sendo criado ao mesmo tempo
            livro_generico = Livro.objects.filter(google_id=google_id).first()
            if livro_generico:
                LivroUsuario.objects.get_or_create(user=request.user, livro=livro_generico)
                messages.success(request, 'Livro adicionado (resolvido conflito).')
            else:
                messages.error(request, 'Erro de banco ao salvar o livro.')
        except Exception as e:
            messages.error(request, f'Erro ao salvar o livro: {e}')

        return redirect('minha_estante')

    return redirect('minha_estante')

@login_required
def cadastro_manual(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            novo_livro = form.save()
            LivroUsuario.objects.get_or_create(user=request.user, livro=novo_livro)
            messages.success(request, 'Livro cadastrado manualmente!')
            return redirect('minha_estante')
    else:
        form = LivroForm()
    return render(request, 'livros/cadastro_manual.html', {'form': form})

@login_required
def editar_livro(request, livro_usuario_id):
    relacao = get_object_or_404(LivroUsuario, id=livro_usuario_id, user=request.user)
    if request.method == 'POST':
        relacao.status = request.POST.get('status')
        relacao.nota = request.POST.get('nota') or None
        relacao.comentario = request.POST.get('comentario')
        relacao.data_leitura = request.POST.get('data_leitura') or None
        relacao.save()
        messages.success(request, 'Livro atualizado com sucesso!')
        return redirect('minha_estante')
    else:
        return render(request, 'livros/editar.html', {'relacao': relacao})

@login_required
def remover_livro(request, livro_usuario_id):
    relacao = get_object_or_404(LivroUsuario, id=livro_usuario_id, user=request.user)
    relacao.delete()
    messages.success(request, 'Livro removido da sua estante.')
    return redirect('minha_estante')

@login_required
def sugestoes_para_mim(request):
    sugestoes = gerar_sugestoes(request.user)
    return render(request, 'livros/sugestoes.html', {'sugestoes': sugestoes})
