from django import forms
from .models import InfoPageModel


class EditPageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
            }
        ),
        label='Содержание страницы (HTML)',
    )
    title = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Имя страницы',
    )
    class Meta:
        model = InfoPageModel
        fields = ['content', 'title']
