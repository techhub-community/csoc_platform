from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class Program(models.Model):
    name = models.CharField(max_length=128)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    program_selected = models.ForeignKey(Program, null=True, on_delete=models.SET_NULL)
    techstack = models.TextField(_("Techstack"), null=True, default=None, blank=True)
    phone_number = PhoneNumberField()
    usn = models.CharField(max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Proficiency(models.TextChoices):
        EXPERT = 'EXP', _('Expert')
        BEGINNER = 'BEG', _('Beginner')
        GOOD = 'GOO', _('Good')
        AVERAGE = 'AVG', _('Average')

    proficiency = models.CharField(
        max_length=3,
        choices=Proficiency.choices,
        default=Proficiency.BEGINNER,
    )

    objects = CustomUserManager()
