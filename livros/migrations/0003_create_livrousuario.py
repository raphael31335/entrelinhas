# Generated manually: cria o modelo LivroUsuario com unique_together (user, livro)
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('livros', '0002_remove_livrousuario_unique_user_livro_and_more'),  # ajuste se necessário
    ]

    operations = [
        migrations.CreateModel(
            name='LivroUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Lido','Lido'), ('Lendo','Lendo'), ('Desejo ler','Desejo ler')], max_length=20)),
                ('nota', models.IntegerField(blank=True, null=True)),
                ('comentario', models.TextField(blank=True)),
                ('data_leitura', models.DateField(blank=True, null=True)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livros.livro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='livrousuario',
            unique_together={('user', 'livro')},
        ),
    ]
