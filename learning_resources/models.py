from django.db import models


class Resource(models.Model):
    DOMAIN_CHOICES = (
        ('dsa', 'DSA'),
        ('web', 'Web'),
        ('app', 'App'),
        ('ui', 'UI/UX'),
    )

    domain = models.CharField(choices=DOMAIN_CHOICES, max_length=3)
    topic = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return f"{self.domain} - {self.topic} - {self.name}"
