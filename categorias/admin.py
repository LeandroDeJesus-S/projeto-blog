from django.contrib import admin
from .models import Categoria


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoria']
    list_display_links = ['id', 'categoria']


admin.site.register(Categoria, CategoriaAdmin)
