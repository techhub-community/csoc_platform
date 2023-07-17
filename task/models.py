from django.db import models
from user.models import User , Member
from django.utils.translation import gettext as _


class Task(models.Model):
    
    team = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team} {self.detail}"

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskStatus(models.Model):
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.BooleanField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} {self.status} {self.member}"

    class Meta:
        verbose_name = 'Task Status'
        verbose_name_plural = 'Task Statuses'


class Badge(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} {self.badge_name}"

    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'


