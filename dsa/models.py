from django.db import models


class Topic(models.Model):
    topic_name = models.CharField(max_length=100)

    def __str__(self):
        return self.topic_name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
