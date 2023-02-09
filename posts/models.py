from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(default=timezone.now)
    conteudo = models.TextField()
    excerto = models.TextField()
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, blank=True, null=True)
    imagem = models.ImageField(upload_to='post/img/%Y/%b/%d', blank=True, null=True)
    publicado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.titulo
