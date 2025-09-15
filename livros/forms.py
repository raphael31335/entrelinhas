# livros/forms.py
from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['google_id', 'titulo', 'autores', 'capa']
