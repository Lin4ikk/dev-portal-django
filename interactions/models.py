from django.db import models
from django.conf import settings
from blog.models import Post

class Comment(models.Model):
    """
    Модель комментариев к статьям.
    Связывает пользователя и статью через ForeignKey (Один-ко-многим).
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Статья"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария"
    )
    text = models.TextField(max_length=1000, verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Комментарий от {self.author.username} к статье {self.post.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']  # Старые комментарии сверху, новые снизу