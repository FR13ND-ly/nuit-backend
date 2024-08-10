from django.db import models
from django.utils import timezone

class Image(models.Model):
    file = models.FileField()
    date = models.DateTimeField(default=timezone.now)

class Item(models.Model):
    cover = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='cover')
    onhover = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    likes = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
