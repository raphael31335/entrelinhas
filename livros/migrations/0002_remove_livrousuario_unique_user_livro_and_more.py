# livros/migrations/0002_create_livrousuario.py
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('livros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LivroUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Lido', 'Lido'), ('Lendo', 'Lendo'), ('Desejo ler', 'Desejo ler')], max_length=20)),
                ('nota', models.IntegerField(blank=True, null=True)),
                ('comentario', models.TextField(blank=True)),
                ('data_leitura', models.DateField(blank=True, null=True)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livros.livro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Livro do Usuário',
                'verbose_name_plural': 'Livros dos Usuários',
            },
        ),
        migrations.AlterUniqueTogether(
            name='livrousuario',
            unique_together={('user', 'livro')},
        ),
    ]
