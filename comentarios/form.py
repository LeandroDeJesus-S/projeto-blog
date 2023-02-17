from django import forms
from .models import Comentario
import requests


class ComentarioForm(forms.ModelForm):
    def clean(self):
        captcha_resp = self.data.get('g-recaptcha-response')
        post_data = {
            'secret': '6Lcrj4skAAAAAJwmGopx9Kehjr_PypTf6VurP3Qn', 
            'response': captcha_resp
        }
        captcha_req = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', 
            data=post_data
        )
        captcha_solved = captcha_req.json()
        if not captcha_solved.get('success'):
            self.add_error('comentario', 'reCaptcha inválido.')
        
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
    
