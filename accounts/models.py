from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
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
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="Пользователь"
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True, 
        verbose_name="Аватар"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг автора")

    def __str__(self):
        return f"Профиль {self.user.username}"

    def update_rating(self):
        total_likes = 0
        posts = self.user.posts.all()
        for post in posts:
            if hasattr(post, 'likes'):
                total_likes += post.likes.count()
        self.rating = total_likes
        self.save()

    def get_role_display_name(self):
        return dict(CustomUser.ROLE_CHOICES).get(self.user.role, "Неизвестно")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()