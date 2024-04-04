from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'categories',
            'content',
        ]

        widgets = {
            'categories': forms.CheckboxSelectMultiple,
            # Изменяем размер поля ввода
            'title': forms.TextInput(attrs={'style': 'width: 40vw'}),
            'content': forms.Textarea(attrs={'style': 'width: 70vw; height: 10em'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            content = cleaned_data.get("content")
            title = cleaned_data.get("title")

            if title == content:
                raise ValidationError(
                    "Содержание не должно быть идентичным названию."
                )

            return cleaned_data
