from django.urls import path
from .views import PostListView, PostDetailView, post_create_view, post_delete_view, comment_delete_view, vote_post

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('category/<int:category_id>/', PostListView.as_view(), name='category_filter'),
    path('post/add/', post_create_view, name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', post_delete_view, name='post_delete'),
    path('comment/<int:pk>/delete/', comment_delete_view, name='comment_delete'),
    path('post/<int:pk>/vote/<str:vote_type>/', vote_post, name='vote_post'),
]