from django import forms
from .models import EESUser, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.images import get_image_dimensions


class UserProfileEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control-plaintext',
        },
    ), required=False)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control-plaintext',
        },
    ), required=False)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control-plaintext',
        },
    ), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control-plaintext',
        },
    ), required=False)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
        ]


class AdminPanelEESUserChangeForm(forms.ModelForm):
    is_admin        = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    is_moderator    = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    is_student      = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    is_employee     = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    is_teacher      = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )

    can_change_email        = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    can_change_username     = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    can_change_first_name   = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )
    can_change_last_name    = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            },
        ),
        required=False,
    )

    class Meta:
        model = EESUser
        fields = [
            'is_admin', 'is_employee', 'is_moderator', 'is_student',
            'is_teacher', 'can_change_email', 'can_change_first_name',
            'can_change_last_name', 'can_change_username',
        ]


class EESUser_Form(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            },
        ),
        required=False
    )
    class Meta:
        model = EESUser
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if avatar:
            try:
                w, h = get_image_dimensions(avatar)

                #validate dimensions
                max_width = max_height = 2000
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Please use an image that is '
                        '%s x %s pixels or smaller.' % (max_width, max_height))

                #validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')

                #validate file size
                if len(avatar) > (20 * 1024 * 50):
                    raise forms.ValidationError(
                        u'Avatar file size may not exceed 20k.')
                


            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass
        else:
            return 'avatars/no_img.png'

        return avatar
