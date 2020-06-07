from django.db import models
from django.contrib.auth.forms import User

# Create your models here.


class NewsModel(models.Model):
    publisher       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=False)
    name            = models.CharField(max_length=2500, blank=True)
    content         = models.TextField(blank=True)
    publish_date    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
