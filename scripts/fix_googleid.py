# scripts/fix_googleid.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entrelinhas.settings")
django.setup()

from livros.models import Livro

def main():
    # converte google_id vazio ('') para None (NULL)
    livros_vazios = Livro.objects.filter(google_id='')
    count = livros_vazios.count()
    if count:
        livros_vazios.update(google_id=None)
        print(f"Converted {count} empty google_id to NULL")
    else:
        print("No empty google_id found")

if __name__ == "__main__":
    main()
