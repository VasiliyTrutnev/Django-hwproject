from django import forms
from .models import Ads, Categories, Profile


class AdForm(forms.ModelForm):

    class Meta:
        model = Ads
        fields = ['description', 'photo_ad', 'title', 'categ']
        labels = {
            'description': 'Описание объявления',
            'photo_ad': 'Выберите файл',
            'title': 'Название объявления',
            'categ': 'Выберите категорию'
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Описание объявления'
            }),
            'photo_ad': forms.ClearableFileInput(attrs={
                'type': 'file', 'class': 'form-control-file'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название объявления'
            }),
            'categ': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Категория объявления'
            })
        }

