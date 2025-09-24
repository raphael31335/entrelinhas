from django import forms
from .models import LivroUsuario


class LivroUsuarioForm(forms.ModelForm):
    class Meta:
        model = LivroUsuario
        fields = ['status', 'nota', 'resenha', 'data_leitura']
