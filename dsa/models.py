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
        return self.question_name

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'


class Status(models.Model):
    class Choices(models.TextChoices):
        PENDING = 'PEN', _('PENDING')
        SUBMITTED = 'SUB', _('SUBMITTED')
        VERIFIED = 'VER', _('VERIFIED')


    choices = models.CharField(
        max_length=3,
        choices=Choices.choices,
        default=Choices.PENDING,
    )

    def __str__(self):
        return self.choices

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Problem_Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Problem Status'
        verbose_name_plural = 'Problem Statuses'

