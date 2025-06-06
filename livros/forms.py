from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['status', 'nota', 'comentario', 'data_leitura']
        widgets = {
            'data_leitura': forms.DateInput(attrs={'type': 'date'}),
        }
