# CONTEÚDO COMPLETO PARA O ARQUIVO: livros/utils.py (ou onde as funções estiverem)

import requests
# Importamos os dois modelos para usar na função gerar_sugestoes
from .models import Livro, LivroUsuario


def buscar_livros_api(termo):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': termo,
        'maxResults': 10,
        'printType': 'books',
        'langRestrict': 'pt'
    }
    resposta = requests.get(url, params=params)

    if resposta.status_code != 200:
        return []

    dados = resposta.json()

    livros = []
    for item in dados.get('items', []):
        volume_info = item.get('volumeInfo', {})
        livro = {
            'titulo': volume_info.get('title'),
            'autores': ', '.join(volume_info.get('authors', [])),
            'descricao': volume_info.get('description', 'Sem descrição'),
            'capa': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'google_id': item.get('id', ''),
        }
        livros.append(livro)

    return livros


def gerar_sugestoes(usuario):
    """
    Função corrigida para funcionar com os modelos Livro e LivroUsuario.
    """
    # 1. Pegar os IDs dos livros que o usuário já tem na estante.
    ids_livros_na_estante = LivroUsuario.objects.filter(user=usuario).values_list('livro_id', flat=True)

    # 2. Buscar os objetos Livro correspondentes a esses IDs.
    livros_na_estante = Livro.objects.filter(id__in=ids_livros_na_estante)

    # 3. Extrair os autores dos livros que o usuário possui.
    autores = set()
    for livro in livros_na_estante:
        if livro.autores:
            autores.update([autor.strip() for autor in livro.autores.split(",")])

    if not autores:
        return [] # Se não houver autores, retorna uma lista vazia.

    # 4. Buscar sugestões na API e filtrar para não mostrar livros que já estão na estante.
    sugestoes = []
    titulos_sugeridos = set() # Usar um set para evitar sugestões duplicadas
    google_ids_na_estante = set(livros_na_estante.values_list('google_id', flat=True))

    for termo in autores:
        livros_encontrados_api = buscar_livros_api(termo)
        for livro_sugerido in livros_encontrados_api:
            # Verifica se o livro já está na estante (pelo google_id) ou se já foi sugerido
            if livro_sugerido['google_id'] not in google_ids_na_estante and livro_sugerido['titulo'] not in titulos_sugeridos:
                sugestoes.append(livro_sugerido)
                titulos_sugeridos.add(livro_sugerido['titulo'])

    return sugestoes
