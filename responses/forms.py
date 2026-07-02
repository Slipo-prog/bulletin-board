from django import forms
from .models import Response


class ResponseForm(forms.ModelForm):
    """
    Форма для создания отклика
    """

    class Meta:
        model = Response
        fields = ['text']
        labels = {
            'text': 'Текст отклика',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Напишите ваш отклик здесь...',
                'required': True,
            }),
        }

    def clean_text(self):
        """
        Валидация текста отклика
        """
        text = self.cleaned_data.get('text')
        if len(text) < 3:
            raise forms.ValidationError('Текст отклика должен содержать минимум 3 символа')
        if len(text) > 1000:
            raise forms.ValidationError('Текст отклика не должен превышать 1000 символов')
        return text