from django.urls import path
from .views import PostListView, PostDetailView, post_create_view # <--- Импортируем функцию вместо класса

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('category/<int:category_id>/', PostListView.as_view(), name='category_filter'),
    path('post/add/', post_create_view, name='post_create'), # <--- Убрали .as_view(), теперь это функция!
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]