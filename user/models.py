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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    objects = CustomUserManager()



class Team(models.Model):
    name = models.CharField(_(""), max_length=50)


# while accepting make sure that accepting from any team is not true
class Member(models.Model):
    user = models.ForeignKey("user.User", verbose_name=_(""), null=True, default=None, on_delete=models.SET_DEFAULT)
    team = models.ForeignKey(Team, verbose_name=_(""), on_delete=models.CASCADE)
    acceptance_status = models.BooleanField(_(""))
