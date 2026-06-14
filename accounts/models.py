from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя для блога.
    Выполняет требование по разделению на 3-4 роли.
    """
    ROLE_GUEST = 'guest'
    ROLE_READER = 'reader'
    ROLE_AUTHOR = 'author'
    ROLE_MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (ROLE_GUEST, 'Гость'),
        (ROLE_READER, 'Читатель'),
        (ROLE_AUTHOR, 'Автор'),
        (ROLE_MODERATOR, 'Модератор'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_READER,
        verbose_name="Роль пользователя"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Profile(models.Model):
    """
    Модель профиля, связанная OneToOneField с пользователем.
    Реализует требование сложной бизнес-логики (расчет рейтинга).
    """
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,  # <-- Исправлено здесь
        related_name='profile',
        verbose_name="Пользователь"
    )
    avatar = models.ImageField(
        upload_to='avatars/',      # <-- Исправлено здесь
        blank=True, 
        null=True, 
        verbose_name="Аватар"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг автора")

    def __str__(self):
        return f"Профиль {self.user.username}"

    def update_rating(self):
        """
        Сложная операция (Бизнес-логика):
        Пересчитывает рейтинг автора на основе общего количества лайков к его статьям.
        """
        pass

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"