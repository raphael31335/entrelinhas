# livros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from django.db import IntegrityError, transaction
import logging

from .models import Livro, LivroUsuario
from .forms import LivroForm
from .utils import buscar_livros_api, gerar_sugestoes

logger = logging.getLogger(__name__)

@login_required
def minha_estante(request):
    relacoes_livros = LivroUsuario.objects.filter(user=request.user).select_related('livro')
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
    """
    Versão mais defensiva para evitar IntegrityError global:
    - normaliza google_id (string vazia -> None)
    - usa get_or_create para Livro e para LivroUsuario
    - transaction.atomic para segurança
    - logging para facilitar debug no Render
    """
    if request.method != 'POST':
        messages.error(request, 'Requisição inválida.')
        return redirect('minha_estante')

    titulo = (request.POST.get('titulo') or '').strip()
    autores = (request.POST.get('autores') or '').strip()
    google_id = request.POST.get('google_id')
    capa = (request.POST.get('capa') or '').strip()

    # Normaliza google_id: considera None se vazio
    if google_id is not None:
        google_id = google_id.strip()
        if google_id == '':
            google_id = None

    if not titulo:
        messages.error(request, 'Título inválido.')
        return redirect('minha_estante')

    try:
        with transaction.atomic():
            if google_id:
                livro_generico, created_livro = Livro.objects.get_or_create(
                    google_id=google_id,
                    defaults={'titulo': titulo, 'autores': autores, 'capa': capa}
                )
            else:
                # Se não há google_id, cria/pega por título (evita duplicates vazios)
                livro_generico, created_livro = Livro.objects.get_or_create(
                    titulo=titulo,
                    defaults={'autores': autores, 'capa': capa}
                )

            relacao, relacao_criada = LivroUsuario.objects.get_or_create(
                user=request.user,
                livro=livro_generico
            )

            if relacao_criada:
                messages.success(request, f'Livro "{livro_generico.titulo}" salvo na sua estante.')
            else:
                messages.warning(request, f'Já existe este livro na sua estante.')

            logger.info(
                "salvar_livro_api: user=%s livro_id=%s created_livro=%s relacao_criada=%s",
                request.user.username, livro_generico.id, created_livro, relacao_criada
            )

    except IntegrityError as e:
        logger.exception("IntegrityError ao salvar livro para usuário %s: %s", request.user.username, str(e))
        messages.error(request, 'Erro de banco ao salvar o livro.')
    except Exception as e:
        logger.exception("Erro inesperado em salvar_livro_api: %s", str(e))
        messages.error(request, 'Erro inesperado ao salvar o livro.')

    return redirect('minha_estante')

@login_required
def cadastro_manual(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            novo_livro = form.save()
            LivroUsuario.objects.create(user=request.user, livro=novo_livro)
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

# -------------------------
# Debug view (temporária) - REMOVA APÓS TESTES
# -------------------------
@staff_member_required
def debug_db_status(request):
    total_livros = Livro.objects.count()
    total_relacoes = LivroUsuario.objects.count()
    livros_com_google_vazio = Livro.objects.filter(google_id='').count()
    ultimos_livros = Livro.objects.order_by('-id')[:20]
    ultimas_relacoes = LivroUsuario.objects.order_by('-id')[:20]

    lines = [
        f"total_livros={total_livros}",
        f"total_livro_usuario={total_relacoes}",
        f"livros_com_google_id_vazio={livros_com_google_vazio}",
        "",
        "Últimos Livros:",
    ]
    for l in ultimos_livros:
        lines.append(f"{l.id} | titulo={l.titulo} | google_id={l.google_id!r} | capa={l.capa or '-'}")

    lines.append("")
    lines.append("Últimas Relações (LivroUsuario):")
    for r in ultimas_relacoes:
        lines.append(f"{r.id} | user={r.user.username} | livro_id={r.livro.id} | livro_titulo={r.livro.titulo}")

    return HttpResponse("<br>".join(lines))
