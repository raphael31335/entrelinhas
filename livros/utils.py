# livros/utils.py
import requests

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

def buscar_livros_api(termo, max_results=10):
    """
    Busca no Google Books e retorna uma lista de dicionários:
    { 'titulo', 'autores', 'google_id', 'capa' }
    """
    if not termo:
        return []
    params = {
        "q": termo,
        "maxResults": max_results,
    }
    try:
        resp = requests.get(GOOGLE_BOOKS_API, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        resultados = []
        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            titulo = info.get("title", "Sem título")
            autores = ", ".join(info.get("authors", []))
            imagens = info.get("imageLinks", {}) or {}
            capa = imagens.get("thumbnail", "")
            google_id = item.get("id")
            resultados.append({
                "titulo": titulo,
                "autores": autores,
                "capa": capa,
                "google_id": google_id,
            })
        return resultados
    except Exception:
        # se algo falhar, retorna lista vazia (o front já lida com isso)
        return []

def gerar_sugestoes(user, limit=6):
    """
    Retorna queryset/lista de objetos Livro como sugestão.
    Estratégia simples: pega livros que o usuário ainda não tem.
    """
    from .models import Livro, LivroUsuario

    user_livro_ids = LivroUsuario.objects.filter(user=user).values_list("livro_id", flat=True)
    sugestoes = Livro.objects.exclude(id__in=user_livro_ids).order_by('?')[:limit]
    return sugestoes
