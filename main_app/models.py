from django.db import models

# Create your models here.


class InfoPageManager(models.Manager):
    def create_page(self, name, title=None):
        if not title:
            title = name
        page = self.create(name=name, title=title)
        page.save()
        return page

    def get_or_create_page(self, name, title=None):
        try:
            page = self.get(name=name)
        except InfoPageModel.DoesNotExist:
            page = self.create_page(name=name, title=title)
        return page


class InfoPageModel(models.Model):
    name    = models.CharField(max_length=30, unique=True, null=False)
    content = models.TextField(null=True, blank=True)
    title   = models.CharField(max_length=30, null=True, blank=True)

    objects = InfoPageManager()

    def __str__(self):
        return self.name
