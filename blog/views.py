from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .models import Post, Tag, Category
from .forms import PostCreateForm
from interactions.models import Comment
from interactions.forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'     
    paginate_by = 5                   

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True).select_related('author', 'category')
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_id'] = self.kwargs.get('category_id')
        return context

class PostDetailView(FormMixin, DetailView):
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
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_published = True 
            post.save()
            
            tags_data = form.cleaned_data.get('tags_str', '')
            if tags_data:
                from django.utils.text import slugify
                tag_list = [t.strip().lower() for t in tags_data.split(',') if t.strip()]
                
                for tag_name in tag_list:
                    tag_slug = slugify(tag_name)
                    if not tag_slug:
                        tag_slug = tag_name
                        
                    tag, created = Tag.objects.get_or_create(
                        title=tag_name,
                        defaults={'slug': tag_slug}
                    )
                    post.tags.add(tag)
            
            return redirect('blog:home')
    else:
        form = PostCreateForm()
        
    return render(request, 'blog/post_form.html', {'form': form})

@login_required(login_url='accounts:login')
def post_delete_view(request, pk):
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user and not request.user.is_staff:
        raise PermissionDenied
        
    if request.method == 'POST':
        post.delete()
        return redirect('blog:home')
        
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required(login_url='accounts:login')
def comment_delete_view(request, pk):
    from django.shortcuts import get_object_or_404
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user and not request.user.is_staff:
        raise PermissionDenied
        
    if request.method == 'POST':
        post_pk = comment.post.pk
        comment.delete()
        return redirect('blog:post_detail', pk=post_pk)
        
    return redirect('blog:home')