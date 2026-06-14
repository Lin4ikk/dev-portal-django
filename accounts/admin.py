from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения пользователей в панели администратора."""
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля (Роли)', {'fields': ('role',)}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Настройка отображения профилей в админке."""
    list_display = ['user', 'rating']
    search_fields = ['user__username']