import requests

def buscar_livros_api(termo):
    if not termo:
        return []
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": termo, "maxResults": 10}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        resultados = []
        for item in data.get('items', []):
            info = item.get('volumeInfo', {})
            resultados.append({
                'titulo': info.get('title'),
                'autores': ', '.join(info.get('authors', [])),
                'capa': (info.get('imageLinks') or {}).get('thumbnail', ''),
                'google_id': item.get('id'),
            })
        return resultados
    except Exception:
        return []
