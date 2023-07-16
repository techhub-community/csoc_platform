from django.db import models
from user.models import User
# from django.utils.translation import gettext as _

# Create your models here.


class Contest(models.Model):
    contest_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    no_of_problems = models.IntegerField()

    def __str__(self):
        return f'{self.contest_name}'

    class Meta:
        verbose_name = 'Contest'
        verbose_name_plural = 'Contests'


class Participation(models.Model):
    problem_solved = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    rank = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.contest.contest_name}'

    class Meta:
        verbose_name = 'Participation'
        verbose_name_plural = 'Participations'