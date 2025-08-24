from django import forms
from .models import News

class AddPostForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'image', 'newstopic']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'title-input',
                'placeholder': 'Введите заголовок статьи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите содержание статьи'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'newstopic': forms.Select(attrs={
                'class': 'form-control'
            }),
        }