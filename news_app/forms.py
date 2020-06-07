from django.forms import Form, ModelForm
from django import forms
from .models import NewsModel


class EditNewsForm(ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
            }
        ),
        label='Содержание новости',
    )
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Название новости',
    )
    class Meta:
        model = NewsModel
        fields = ['content', 'name']
