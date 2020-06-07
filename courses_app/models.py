from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SectionModel(models.Model):
    name = models.CharField(max_length=40, null=True)


class CourseModel(models.Model):
    name                = models.CharField(max_length=60)
    section             = models.OneToOneField(SectionModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TestsModel(models.Model):
    name                = models.CharField(max_length=60)
    description         = models.TextField(blank=True)
    number_of_questions = models.IntegerField(null=True)
    tries               = models.IntegerField(null=True)
    time_restriction    = models.IntegerField(null=True)

    section = models.ForeignKey(SectionModel, on_delete=models.CASCADE)


class QuestionModel(models.Model):
    type        = models.CharField(max_length=2, null=False)
    rating      = models.FloatField(null=False)
    question    = models.TextField(null=False)
    hint        = models.TextField(blank=True)
    test        = models.ForeignKey(TestsModel, on_delete=models.CASCADE)


class CheckOrRadioAnswerModel(models.Model):
    text        = models.TextField(null=False)
    is_correct  = models.BooleanField(default=False, null=False)
    question    = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)


class Question2Group(models.Model):
    question    = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    group       = models.TextField()


class DocumentsModel(models.Model):
    name        = models.CharField(max_length=40)
    document    = models.FileField(upload_to='documents/')
    section     = models.ForeignKey(SectionModel, on_delete=models.CASCADE)


class PagesModel(models.Model):
    name    = models.CharField(max_length=40, null=False)
    content = models.TextField(null=True)
    section = models.ForeignKey(SectionModel, on_delete=models.CASCADE)


class Section2Sections(models.Model):
    section     = models.ForeignKey(SectionModel, on_delete=models.CASCADE)
    sections    = models.OneToOneField(SectionModel, on_delete=models.CASCADE, related_name='section_of_this_section')


class Course2Student(models.Model):
    course  = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Course2Employee(models.Model):
    course      = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    employee    = models.ForeignKey(User, on_delete=models.CASCADE)


class Course2Teacher(models.Model):
    course  = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)


class TriesModel(models.Model):
    student         = models.ForeignKey(User, on_delete=models.CASCADE)
    test            = models.ForeignKey(TestsModel, on_delete=models.CASCADE)
    date_started    = models.DateTimeField(auto_now_add=True)
    date_submitted   = models.DateTimeField(null=True, default=None)
    rated           = models.BooleanField(default=False, null=False)
    max_rating      = models.FloatField(default=None, null=True)
    rating          = models.FloatField(default=None, null=True)


class Try2Question(models.Model):
    try_field   = models.ForeignKey(TriesModel, on_delete=models.CASCADE)
    question    = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    answer      = models.TextField(null=True, default=None)
    answer_file = models.FileField(upload_to='answers/', null=True)
    rate        = models.FloatField(null=True, default=None)
