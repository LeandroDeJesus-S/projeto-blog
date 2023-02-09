from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.categoria
