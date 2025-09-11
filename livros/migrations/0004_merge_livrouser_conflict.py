# livros/migrations/0004_merge_livrouser_conflict.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0002_remove_livrousuario_unique_user_livro_and_more'),
        ('livros', '0003_create_livrousuario'),
    ]

    operations = [
        # Esta migration apenas resolve o grafo de dependências (merge).
        # Nenhuma operação no esquema é necessária aqui.
    ]
