from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .models import Post, Tag
from .forms import PostCreateForm
from interactions.models import Comment
from interactions.forms import CommentForm


class PostListView(ListView):
    """Представление для главной страницы с фильтрацией по категориям"""
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'     
    paginate_by = 5                   

    def get_queryset(self):
        # Базовый запрос: только опубликованные статьи
        queryset = Post.objects.filter(is_published=True).select_related('author', 'category')
        
        # Проверяем, передан ли ID категории в URL (например, /category/1/)
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        """Передаем список всех категорий в шаблон, чтобы отобразить меню"""
        context = super().get_context_data(**kwargs)
        from .models import Category
        context['categories'] = Category.objects.all()
        context['current_category_id'] = self.kwargs.get('category_id')
        return context


class PostDetailView(FormMixin, DetailView):
    """Представление для детальной страницы статьи с комментариями"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        if self.request.user.is_authenticated:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        """Обработка отправки нового комментария"""
        if not request.user.is_authenticated:
            raise PermissionDenied
        
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object          
        comment.author = self.request.user  
        comment.save()
        return redirect('blog:post_detail', pk=self.object.pk)


@login_required(login_url='accounts:login')
def post_create_view(request):
    """Стабильная функция для создания статьи и добавления хэштегов на лету."""
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            # 1. Создаем объект статьи, но пока не сохраняем в БД
            post = form.save(commit=False)
            # 2. Вручную привязываем текущего автора
            post.author = request.user
            post.is_published = True 
            # 3. Сохраняем статью в базу данных (теперь у неё есть уникальный ID)
            post.save()
            
            # 4. Обрабатываем текстовую строку с хэштегами
            tags_data = form.cleaned_data.get('tags_str', '')
            if tags_data:
                # Разбиваем по запятым, очищаем пробелы и переводим в нижний регистр
                tag_list = [t.strip().lower() for t in tags_data.split(',') if t.strip()]
                
                for tag_name in tag_list:
                    # Ищем тег, либо автоматически создаем новый
                    tag, created = Tag.objects.get_or_create(title=tag_name)
                    # Привязываем хэштег к статье
                    post.tags.add(tag)
            
            # 5. Перенаправляем на детальную страницу новой статьи
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostCreateForm()
        
    return render(request, 'blog/post_form.html', {'form': form})