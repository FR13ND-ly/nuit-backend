from django.db import models
from django.utils import timezone

class Item(models.Model):
    likes = models.PositiveIntegerField(default=0)
    file = models.FileField()
    date = models.DateTimeField(default=timezone.now)
