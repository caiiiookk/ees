from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User

# Create your models here.


class EESUser(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin                = models.BooleanField(default=False)
    is_employee             = models.BooleanField(default=False)
    is_teacher              = models.BooleanField(default=False)
    is_student              = models.BooleanField(default=False)
    is_moderator            = models.BooleanField(default=False)
    can_change_username     = models.BooleanField(default=False)
    can_change_email        = models.BooleanField(default=True)
    can_change_first_name   = models.BooleanField(default=True)
    can_change_last_name    = models.BooleanField(default=True)
    avatar                  = models.ImageField(null=False, default='no_img.png', upload_to='avatars')

    def __str__(self):
        return self.user.username
