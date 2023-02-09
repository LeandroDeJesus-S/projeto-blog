from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone

class Comentario(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    email = models.EmailField(verbose_name='E-mail')
    comentario = models.TextField(verbose_name='Comentário')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)
    publicado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
