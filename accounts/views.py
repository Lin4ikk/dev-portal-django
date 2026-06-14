from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm

class RegisterView(CreateView):
    """Представление для регистрации нового пользователя."""
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')  # После успешной регистрации отправляем на страницу входа

class MyLoginView(LoginView):
    """Представление для авторизации (входа)."""
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        # После входа перенаправляем на главную страницу блога
        return reverse_lazy('blog:home')

class MyLogoutView(LogoutView):
    """Представление для выхода из системы."""
    next_page = reverse_lazy('blog:home')  # После выхода возвращаем на главную

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin # Защита страницы от гостей

class ProfileView(LoginRequiredMixin, TemplateView):
    """Страница личного кабинета пользователя."""
    template_name = 'accounts/profile.html'