from django import forms
from .models import (
    CourseModel,
    SectionModel,
    DocumentsModel,
    PagesModel,
    TestsModel,
    CheckOrRadioAnswerModel,
    QuestionModel,
    TriesModel,
    Try2Question,
)


class EditCourseForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'rows': 3,
            }
        ),
        label='Название курса',
        required=True,
    )

    class Meta:
        model = CourseModel
        fields = ['name']


class EditSectionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Название раздела',
        required=True,
    )
    class Meta:
        model = SectionModel
        fields = ['name']


class EditPageForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Название страницы',
        required=True,
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
            }
        ),
        label='Содержание страницы (HTML)',
        required=True,
    )
    class Meta:
        model = PagesModel
        fields = ['name', 'content']


class EditDocumentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Название файла',
        required=True,
    )
    document = forms.FileField(
        required=True,)
    class Meta:
        model = DocumentsModel
        fields = ['name', 'document']


class EditTestForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Название теста',
        required=True,
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Описание теста',
        required=False,
    )
    number_of_questions = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Количество вопросов',
        required=False,
        help_text='Если не задано - будет по одному на каждый имеющийся номер вопроса, либо, если не заданы номера вопроса - все',
    )
    tries = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Количество попыток',
        required=False,
        help_text='Если не задано - сколько угодно',
    )
    time_restriction = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Ограничение по времени',
        required=False,
        help_text='В минутах',
    )

    class Meta:
        model = TestsModel
        fields = ['name', 'description', 'number_of_questions', 'tries', 'time_restriction']


class EditAnswerForm(forms.ModelForm):
    text  = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Ответ на вопрос',
        required=True,
    )
    is_correct   = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check',
            }
        ),
        label='Правильный ответ',
        required=False,
    )

    class Meta:
        model = CheckOrRadioAnswerModel
        fields = ['text', 'is_correct']


class EditQuestionForm(forms.ModelForm):
    type        = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-group',
            },
        ),
        label='Тип',
    )
    question    = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Содержание вопроса',
        required=True,
    )
    hint        = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Подсказки проверяющему',
        required=False,
    )
    rating      = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            },
        ),
        label='Баллов за вопрос',
        required=True,
    )

    class Meta:
        model = QuestionModel
        fields = ['type', 'question', 'hint', 'rating']


class UserQuestionCheckForm(forms.ModelForm):
    answer = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            # 'class': 'form-control',
        }),
        label='Ответ',
        required=False,
    )

    class Meta:
        model = Try2Question
        fields = ['answer']


class UserQuestionRadioForm(forms.ModelForm):
    answer = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
            # 'class': 'form-control',
        }),
        label='Ответ',
        required=False,
    )

    class Meta:
        model = Try2Question
        fields = ['answer']


class UserQuestionInputForm(forms.ModelForm):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={
            # 'class': 'form-control',
        }),
        label='Ответ',
        required=False,
    )

    class Meta:
        model = Try2Question
        fields = ['answer']


class UserQuestionFileForm(forms.ModelForm):
    answer_file = forms.FileField(
        label='Ответ',
        required=False,
        widget=forms.FileInput(attrs={
            # 'class': 'form-control',
        }),
    )

    class Meta:
        model = Try2Question
        fields = ['answer_file']


class EmployeeRateForm(forms.ModelForm):
    rate = forms.FloatField(
        required=True,
    )

    class Meta:
        model = Try2Question
        fields = ['rate']
