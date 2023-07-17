from django.db import models
from user.models import Member, Team
from django.utils.translation import gettext as _


class Task(models.Model):    
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team} {self.detail}"

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskStatus(models.Model):    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} {self.status} {self.member}"

    class Meta:
        verbose_name = 'Task Status'
        verbose_name_plural = 'Task Statuses'