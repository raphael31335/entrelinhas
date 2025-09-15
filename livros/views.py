from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro, LivroUsuario
from .forms import LivroForm
from .utils import buscar_livros_api, gerar_sugestoes
from django.db import transaction, IntegrityError

@login_required
def salvar_livro_api(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autores = request.POST.get('autores')
        google_id = request.POST.get('google_id')
        capa = request.POST.get('capa')

        try:
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
                    messages.success(request, 'Livro salvo na sua estante!')
                else:
                    messages.warning(request, 'Este livro já está na sua estante.')

        except IntegrityError:
            # evita crash em casos de corrida/duplicata
            messages.error(request, 'Erro de banco ao salvar o livro. Tente novamente.')
        except Exception as e:
            messages.error(request, f'Erro ao salvar o livro: {e}')

    return redirect('minha_estante')
