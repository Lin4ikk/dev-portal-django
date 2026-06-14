import math
from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Модель категории статей.
    Связь Один-ко-многим (ForeignKey) с моделью Post.
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
    Связь Многие-ко-многим (ManyToMany) с моделью Post.
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
    Основная модель статьи (поста) в блоге.
    Связывает пользователя (автора), категорию и теги.
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
    
    # Поле ManyToMany для хранения лайков от пользователей
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
        Сложная операция (Бизнес-логика):
        Рассчитывает примерное время чтения статьи в минутах.
        Средняя скорость чтения — 200 слов в минуту.
        """
        words = self.content.split()
        words_count = len(words)
        read_time = math.ceil(words_count / 200)
        return read_time if read_time > 0 else 1

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']  # Свежие статьи всегда сверху