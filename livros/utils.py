import requests
from .models import Livro


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
    livros_na_estante = Livro.objects.filter(user=usuario)

    autores = set()
    for livro in livros_na_estante:
        if livro.autores:
            autores.update([autor.strip() for autor in livro.autores.split(",")])

    sugestoes = []
    for termo in autores:
        livros_encontrados = buscar_livros_api(termo)
        for livro in livros_encontrados:
            ja_existe = livros_na_estante.filter(titulo=livro['titulo']).exists()
            if not ja_existe and livro not in sugestoes:
                sugestoes.append(livro)

    return sugestoes
