from django.db import models
from django.contrib.auth.models import User


class Livro(models.Model):
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    titulo = models.CharField(max_length=255)
    autores = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    capa_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.titulo


class LivroUsuario(models.Model):
    STATUS_CHOICES = [
        ('lendo', 'Lendo'),
        ('lido', 'Lido'),
        ('quero_ler', 'Quero Ler'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='quero_ler')
    nota = models.IntegerField(null=True, blank=True)
    resenha = models.TextField(null=True, blank=True)
    data_leitura = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'livro')

    def __str__(self):
        return f"{self.user.username} - {self.livro.titulo}"
