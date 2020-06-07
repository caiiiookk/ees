from django.contrib import admin
from .models import (
    CourseModel,
    SectionModel,
    Section2Sections,
    TestsModel,
    DocumentsModel,
    PagesModel,
    Try2Question,
    QuestionModel,
    TriesModel,
)

# Register your models here.

admin.site.register(CourseModel)
admin.site.register(SectionModel)
admin.site.register(Section2Sections)
admin.site.register(TestsModel)
admin.site.register(DocumentsModel)
admin.site.register(PagesModel)
admin.site.register(Try2Question)
admin.site.register(QuestionModel)
admin.site.register(TriesModel)
