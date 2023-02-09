from django.contrib import admin
from .models import Comentario

class ComentarioAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome', 'email', 'post', 'data', 'publicado'
    list_editable = 'publicado',
    list_display_links = 'id', 'nome', 'email'


admin.site.register(Comentario, ComentarioAdmin)
