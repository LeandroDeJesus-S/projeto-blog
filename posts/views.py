from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Case, When, Count
from comentarios.form import ComentarioForm
from comentarios.models import Comentario
from django.contrib import messages
from django.views import View


class PostIndex(ListView):
    model = Post
    template_name = 'posts.html'
    paginate_by = 6
    context_object_name = 'posts'
    ordering = 'id'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria')
        qs = qs.annotate(
            num_comentarios=Count(
                Case(
                    When(comentario__publicado=True, then=1)
                )
            )
        )
        return qs


class PostBusca(PostIndex):
    template_name = 'post_busca.html'
    
    def get_queryset(self):
        busca = self.request.GET.get('termo')
        qs = super().get_queryset()
        if not busca:
            return qs
        qs = qs.filter(
            Q(categoria__categoria__icontains=busca)|
            Q(titulo__icontains=busca)|
            Q(autor__first_name__iexact=busca)|
            Q(conteudo__icontains=busca)|
            Q(excerto__icontains=busca)
        )
        return qs


class PostCategoria(PostIndex):
    template_name = 'post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)
        if categoria is None:
            return qs
        
        qs = qs.filter(categoria__categoria__iexact=categoria)
        
        return qs


# class PostDetalhes(UpdateView):
#     template_name = 'post_detalhes.html'
#     model = Post
#     form_class = ComentarioForm
#     context_object_name = 'post'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comentarios = Comentario.objects.filter(publicado=True,
#                                                 post=post.id)
#         context['comentarios'] = comentarios
#         return context

#     def form_valid(self, form):
#         post = self.get_object()
#         comentario = Comentario(**form.cleaned_data)
#         user = self.request.user
#         comentario.post = post
#         if user.is_authenticated:
#             comentario.usuario = user
        
#         comentario.save()
#         messages.success(self.request, 'Comentário enviado para análise.')
#         return redirect('post_detalhes', pk=post.id)


class PostDetalhes(View):
    template_name = 'post_detalhes.html'
    
    def setup(self, request, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        self.context = {
            'post': post,
            'comentarios': Comentario.objects.filter(publicado=True, post=post),
            'form': ComentarioForm(request.POST or None)
        }
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        self.context = {
            'post': post,
            'comentarios': Comentario.objects.filter(publicado=True, post=post),
            'form': ComentarioForm(request.POST or None)
        }
        return render(request, self.template_name, self.context)
        
    def post(self, request, *args, **kwargs):
        form = self.context['form']
        if not form.is_valid():
            return render(request, self.template_name, self.context)
        comentario = form.save(commit=False)
        if request.user.is_authenticated:
            comentario.usuario = request.user
        comentario.post = self.context['post']
        comentario.save()
        messages.success(request, 'Comentário enviado para revisão.')
        return redirect('post_detalhes', pk=self.kwargs.get('pk'))
        
    
