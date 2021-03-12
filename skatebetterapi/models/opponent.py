
from django.db import models
from .skater import Skater


class Skater(models.Model):

    skater = models.ForeignKey(Skater, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50)
    goofy = models.BooleanField(default=False)