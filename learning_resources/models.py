from django.db import models

from user.models import Program

class Resource(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.topic
