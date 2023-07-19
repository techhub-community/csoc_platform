from django.db import models
from django.utils.translation import gettext as _

from user.models import Member, Team



class TaskStatus(models.Model):
    class Choices(models.TextChoices):
        PENDING = 'PEN', _('PENDING')
        SUBMITTED = 'SUB', _('SUBMITTED')
        VERIFIED = 'VER', _('VERIFIED')
            
    task = models.ForeignKey("task.Task", on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=Choices.choices, default=Choices.PENDING)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} {self.status} {self.member}"

    class Meta:
        verbose_name = 'Task Status'
        verbose_name_plural = 'Task Statuses'
        

class Task(models.Model):
    task_name = models.CharField(max_length=100, default="")   
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.task_name}"
    
    def get_task_status(self, user):
        try:
            member = Member.objects.get(user=user, acceptance_status=True)
            status = TaskStatus.objects.get(task=self, member=member).status
            return status
        except:
            return TaskStatus.Choices.PENDING

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
