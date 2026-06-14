from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    """Форма для создания статьи с вводом хэштегов через запятую."""
    
    # Кастомное текстовое поле для хэштегов
    tags_str = forms.CharField(
        required=False,
        label="Хэштеги",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ведите теги через запятую (например: python, django, код)'
        }),
        help_text="Если тега нет в базе, сайт создаст его автоматически!"
    )

    class Meta:
        model = Post
        # Исключаем оригинальное поле tags из автоматического рендеринга формы
        fields = ['title', 'content', 'category']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите захватывающий заголовок статьи...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Напишите текст вашей публикации...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }