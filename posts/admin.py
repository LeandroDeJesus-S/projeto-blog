from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ['id', 'titulo', 'autor', 'data', 'categoria', 'publicado']
    list_display_links = ['id', 'titulo', 'autor']
    list_editable = ['publicado']
    summernote_fields = 'conteudo',


admin.site.register(Post, PostAdmin)
