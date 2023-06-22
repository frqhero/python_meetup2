from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'
