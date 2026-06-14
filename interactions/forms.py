from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Форма для добавления комментария к публикации."""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите, что вы думаете об этой статье...'
            }),
        }