from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class Program(models.Model):
    name = models.CharField(max_length=128)

class User(AbstractUser):
    username=None
    email=models.EmailField(_('email address'), unique=True)
    password=models.CharField(max_length=128)
    program_selected=models.ForeignKey(Program, null=True, on_delete=models.SET_NULL)
    phone_number= PhoneNumberField()
    usn = models.CharField(max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()