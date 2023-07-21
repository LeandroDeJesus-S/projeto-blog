from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from PIL import Image


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

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        try:
            self.auto_resize_image()
        except Exception as error:
            print(error)
        
    def auto_resize_image(self):
        NEW_WIDTH = 400
        image_path = settings.MEDIA_ROOT / self.imagem.name
        img = Image.open(image_path)
        width, heinght = img.size
        new_heinght = round(NEW_WIDTH * heinght / width)
        if NEW_WIDTH >= width:
            return
        
        new_image = img.resize((NEW_WIDTH, new_heinght), Image.ANTIALIAS)
        new_image.save(image_path, optimize=True, quality=70)
        img.close()
        new_image.close()
