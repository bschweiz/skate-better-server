
from django.db import models
from django.contrib.auth.models import User


class Skater(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50)
    goofy = models.BooleanField(default=False)
    fav_skater = models.CharField(max_length=50)
    fav_video = models.CharField(max_length=50)