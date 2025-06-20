from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Livro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    autores = models.CharField(max_length=200, blank=True)
    capa = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Lido', 'Lido'), ('Lendo', 'Lendo'), ('Desejo ler', 'Desejo ler')],
        blank=True
    )
    nota = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    data_leitura = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo
