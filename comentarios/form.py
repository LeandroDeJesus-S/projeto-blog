from django import forms
from .models import Comentario


class ComentarioForm(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data
        NOME = data.get('nome')
        nome_len = len(NOME)
        nome_chars = ''.join(NOME.split())
        if nome_len < 3 or not nome_chars.isalpha():
            self.add_error(
                'nome', 
                'O nome precisa ter no minimo 3 caracteres '
                'e ser composto apenas por letras.'
            )
    
    
    class Meta:
        model = Comentario
        fields = 'nome', 'email', 'comentario'
    
