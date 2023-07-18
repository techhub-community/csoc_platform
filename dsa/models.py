from django.db import models
from user.models import User
from django.utils.translation import gettext as _


class Topic(models.Model):
    topic_name = models.CharField(max_length=100)

    def __str__(self):
        return self.topic_name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class Problem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.question_name} {self.topic}"

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'


class Problem_Status(models.Model):
    class Choices(models.TextChoices):
        PENDING = 'PEN', _('PENDING')
        SUBMITTED = 'SUB', _('SUBMITTED')
        VERIFIED = 'VER', _('VERIFIED')        

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=Choices.choices, default=Choices.PENDING)

    class Meta:
        verbose_name = 'Problem Status'
        verbose_name_plural = 'Problem Statuses'
