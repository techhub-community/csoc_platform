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
    program_selected = models.ForeignKey(Program, null=True, blank=True, on_delete=models.SET_NULL)
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
    user = models.ForeignKey("user.User", verbose_name=_(""), null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    team = models.ForeignKey(Team, verbose_name=_(""), on_delete=models.CASCADE)
    acceptance_status = models.BooleanField(_(""), default=False)

    class Meta:
        unique_together = (("user", "team"))

    def clean(self):
        super().clean()
        accepted_count = Member.objects.filter(team=self.team, acceptance_status=True).count()
        if accepted_count >= 3:
            raise ValidationError("The team already has three accepted members.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Invite(models.Model):
    sender = models.ForeignKey(Member,verbose_name=_(""), on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(Member,verbose_name=_(""), on_delete=models.CASCADE,related_name="receiver")
    team = models.ForeignKey(Team,verbose_name=_(""), on_delete=models.CASCADE)


class Inquiry(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
