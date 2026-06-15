import math
from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Модель категории статей.
    """
    title = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-слаг")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    """
    Модель тегов для статей.
    """
    title = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL-слаг")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    """
    Основная модель статьи блога со связями и расчетом метрик.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name="Категория"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='posts',
        blank=True,
        verbose_name="Теги"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст статьи")
    image = models.ImageField(upload_to='blog_covers/', blank=True, null=True, verbose_name="Обложка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
        verbose_name="Лайки"
    )

    def __str__(self):
        return self.title

    def get_read_time(self):
        """
        Рассчитывает примерное время чтения статьи в минутах.
        """
        words = self.content.split()
        words_count = len(words)
        read_time = math.ceil(words_count / 200)
        return read_time if read_time > 0 else 1

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для детального просмотра статьи.
        """
        from django.urls import reverse
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def get_comments_count(self):
        """
        Возвращает общее количество комментариев к статье.
        """
        return self.comments.count()

    def get_rating(self):
        """
        Вычисляет суммарный рейтинг статьи на основе голосов.
        """
        return sum(vote.value for vote in self.post_votes.all())

    def update_author_rating(self):
        """
        Пересчитывает и сохраняет суммарный рейтинг автора в его профиле.
        """
        profile = self.author.profile
        total_rating = 0
        author_posts = self.author.posts.all()
        for p in author_posts:
            total_rating += p.get_rating()
        profile.rating = total_rating
        profile.save()

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']


class Vote(models.Model):
    """
    Промежуточная модель для фиксации голосов пользователей.
    """
    VOTE_CHOICES = (
        (1, 'Вверх'),
        (-1, 'Вниз'),
    )
    user = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete=models.CASCADE, 
        related_name='votes'
    )
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='post_votes'
    )
    value = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')