from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя. 
    Наследуется от встроенной UserCreationForm для автоматической валидации паролей.
    """
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap-классы для красивого отображения полей
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'